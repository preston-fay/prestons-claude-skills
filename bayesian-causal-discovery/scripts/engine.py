#!/usr/bin/env python3
"""
Bayesian Causal Discovery Engine
=================================
Self-contained structure learning using only pandas, numpy, matplotlib.
No external Bayesian libraries required (no bnlearn, pgmpy, scipy).

Algorithms implemented:
  - HillClimb search with BIC scoring
  - PC algorithm (constraint-based)
  - Bootstrap stability analysis
  - Method triangulation and confidence tiering

Usage:
    from engine import CausalDiscoveryEngine

    engine = CausalDiscoveryEngine(config)
    results = engine.run(df)

Author: Kearney AI Skills Library
License: Internal Kearney Use Only
"""

import json
import math
import os
from copy import deepcopy
from collections import defaultdict
from itertools import combinations, permutations

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')


# ════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ════════════════════════════════════════════════════════════════════

DEFAULT_CONFIG = {
    # Data
    'target_variable': None,          # Required: name of target column
    'exogenous_variables': [],        # Variables that cannot be caused by endogenous vars
    'blacklist': [],                  # List of (source, target) tuples to forbid
    'whitelist': [],                  # List of (source, target) tuples to force-include

    # Discretization
    'n_bins': 3,                      # Number of quantile bins (2-5)
    'bin_labels': None,               # Custom bin labels (e.g., ['low', 'mid', 'high'])

    # HillClimb
    'hc_restarts': 3,                 # Number of random restarts
    'hc_max_parents': 3,              # Maximum parents per node

    # PC Algorithm
    'pc_alpha': 0.05,                 # Significance threshold for independence tests
    'pc_max_cond_size': None,         # Max conditioning set size (None = auto)

    # Bootstrap
    'n_bootstrap': 30,                # Number of bootstrap resamples
    'bootstrap_method': 'hillclimb',  # 'hillclimb' or 'pc'

    # Confidence tiering
    'green_threshold': 0.70,          # Bootstrap freq for GREEN tier
    'yellow_threshold': 0.30,         # Bootstrap freq for YELLOW tier
    'min_report_freq': 0.05,          # Minimum bootstrap freq to report

    # Output
    'output_dir': './causal_discovery_output',
    'save_plots': True,
    'plot_style': 'kearney',          # 'kearney' (dark) or 'light'
    'figsize': (14, 10),

    # Kearney branding
    'primary_purple': '#6f42c1',
    'bg_dark': '#1a1a2e',
    'text_light': '#e9ecef',
    'accent_colors': {
        'weather': '#7c8db5',
        'enso': '#8e8e8e',
        'trade': '#9b7dbf',
        'price': '#6f42c1',
        'target': '#FFFFFF',
        'default': '#a0a0c0',
    },
}


# ════════════════════════════════════════════════════════════════════
# STATISTICAL PRIMITIVES
# ════════════════════════════════════════════════════════════════════

def chi2_survival(x: float, dof: int) -> float:
    """
    Chi-square survival function (p-value) using Wilson-Hilferty approximation.
    No scipy required.
    """
    if dof <= 0:
        return 1.0
    if x <= 0:
        return 1.0
    z = ((x / dof) ** (1/3) - (1 - 2 / (9 * dof))) / math.sqrt(2 / (9 * dof))
    p = 0.5 * (1 + math.erf(-z / math.sqrt(2)))
    return max(0.0, min(1.0, p))


def chi_square_test(data: pd.DataFrame, var_x: str, var_y: str,
                    cond_set: list = None) -> tuple:
    """
    Chi-square test of independence (or conditional independence).
    Returns (chi2_statistic, p_value, degrees_of_freedom).
    """
    if cond_set is None or len(cond_set) == 0:
        contingency = pd.crosstab(data[var_x], data[var_y])
        observed = contingency.values.astype(float)
        row_sums = observed.sum(axis=1, keepdims=True)
        col_sums = observed.sum(axis=0, keepdims=True)
        total = observed.sum()
        if total == 0:
            return 0.0, 1.0, 0
        expected = (row_sums * col_sums) / total
        expected = np.where(expected == 0, 1e-10, expected)
        chi2 = ((observed - expected) ** 2 / expected).sum()
        dof = (observed.shape[0] - 1) * (observed.shape[1] - 1)
        p_value = chi2_survival(chi2, dof)
        return chi2, p_value, dof
    else:
        total_chi2 = 0.0
        total_dof = 0
        for _, group in data.groupby(cond_set):
            if len(group) < 5:
                continue
            contingency = pd.crosstab(group[var_x], group[var_y])
            observed = contingency.values.astype(float)
            if observed.shape[0] < 2 or observed.shape[1] < 2:
                continue
            row_sums = observed.sum(axis=1, keepdims=True)
            col_sums = observed.sum(axis=0, keepdims=True)
            total = observed.sum()
            if total == 0:
                continue
            expected = (row_sums * col_sums) / total
            expected = np.where(expected == 0, 1e-10, expected)
            total_chi2 += ((observed - expected) ** 2 / expected).sum()
            total_dof += (observed.shape[0] - 1) * (observed.shape[1] - 1)
        p_value = chi2_survival(total_chi2, total_dof)
        return total_chi2, p_value, total_dof


def mutual_information(data: pd.DataFrame, var_x: str, var_y: str) -> float:
    """Compute mutual information between two discrete variables."""
    contingency = pd.crosstab(data[var_x], data[var_y], normalize=True)
    px = contingency.sum(axis=1)
    py = contingency.sum(axis=0)
    mi = 0.0
    for i in contingency.index:
        for j in contingency.columns:
            pxy = contingency.loc[i, j]
            if pxy > 0 and px[i] > 0 and py[j] > 0:
                mi += pxy * np.log(pxy / (px[i] * py[j]))
    return mi


# ════════════════════════════════════════════════════════════════════
# GRAPH UTILITIES
# ════════════════════════════════════════════════════════════════════

def is_dag(adj_matrix: np.ndarray) -> bool:
    """Check if adjacency matrix represents a DAG (no cycles)."""
    n = adj_matrix.shape[0]
    visited = [False] * n
    rec_stack = [False] * n

    def has_cycle(v):
        visited[v] = True
        rec_stack[v] = True
        for u in range(n):
            if adj_matrix[v, u] == 1:
                if not visited[u]:
                    if has_cycle(u):
                        return True
                elif rec_stack[u]:
                    return True
        rec_stack[v] = False
        return False

    for v in range(n):
        if not visited[v]:
            if has_cycle(v):
                return False
    return True


# ════════════════════════════════════════════════════════════════════
# BIC SCORING
# ════════════════════════════════════════════════════════════════════

def bic_score_node(data: pd.DataFrame, node: str, parents: list,
                   n_samples: int) -> float:
    """BIC score for a single node given its parents."""
    if len(parents) == 0:
        counts = data[node].value_counts()
        n_states = len(counts)
        k = n_states - 1
        ll = (counts * np.log(counts / n_samples + 1e-20)).sum()
    else:
        parent_list = list(parents)
        grouped = data.groupby(parent_list + [node]).size().reset_index(name='count')
        parent_counts = data.groupby(parent_list).size().reset_index(name='parent_count')
        merged = grouped.merge(parent_counts, on=parent_list)
        probs = merged['count'] / merged['parent_count']
        ll = (merged['count'] * np.log(probs + 1e-20)).sum()
        n_parent_configs = len(parent_counts)
        n_states = data[node].nunique()
        k = n_parent_configs * (n_states - 1)
    return ll - (k / 2) * np.log(n_samples)


def bic_score_dag(data: pd.DataFrame, adj_matrix: np.ndarray,
                  variables: list) -> float:
    """Total BIC score for a DAG."""
    n = len(data)
    total = 0.0
    for i, node in enumerate(variables):
        parents = [variables[j] for j in range(len(variables)) if adj_matrix[j, i] == 1]
        total += bic_score_node(data, node, parents, n)
    return total


# ════════════════════════════════════════════════════════════════════
# HILLCLIMB SEARCH
# ════════════════════════════════════════════════════════════════════

def hillclimb_search(data: pd.DataFrame, variables: list,
                     max_parents: int = 3, restarts: int = 3,
                     blacklist: set = None) -> tuple:
    """
    HillClimb search for best-scoring DAG using BIC.
    Returns (adjacency_matrix, bic_score).
    """
    if blacklist is None:
        blacklist = set()
    n_vars = len(variables)
    var_idx = {v: i for i, v in enumerate(variables)}
    bl_idx = {(var_idx.get(s, -1), var_idx.get(t, -1)) for s, t in blacklist}

    best_global_adj = np.zeros((n_vars, n_vars), dtype=int)
    best_global_score = bic_score_dag(data, best_global_adj, variables)

    for restart in range(restarts):
        if restart == 0:
            adj = np.zeros((n_vars, n_vars), dtype=int)
        else:
            adj = np.zeros((n_vars, n_vars), dtype=int)
            for _ in range(np.random.randint(0, n_vars)):
                i, j = np.random.randint(0, n_vars, 2)
                if i != j and (i, j) not in bl_idx:
                    adj[i, j] = 1
                    if not is_dag(adj):
                        adj[i, j] = 0

        current_score = bic_score_dag(data, adj, variables)
        improved = True

        while improved:
            improved = False
            best_delta = 0
            best_op = None

            for i in range(n_vars):
                for j in range(n_vars):
                    if i == j:
                        continue

                    # Try adding edge i → j
                    if adj[i, j] == 0 and (i, j) not in bl_idx:
                        n_parents = adj[:, j].sum()
                        if n_parents < max_parents:
                            adj[i, j] = 1
                            if is_dag(adj):
                                new_score = bic_score_dag(data, adj, variables)
                                delta = new_score - current_score
                                if delta > best_delta:
                                    best_delta = delta
                                    best_op = ('add', i, j)
                            adj[i, j] = 0

                    # Try removing edge i → j
                    if adj[i, j] == 1:
                        adj[i, j] = 0
                        new_score = bic_score_dag(data, adj, variables)
                        delta = new_score - current_score
                        if delta > best_delta:
                            best_delta = delta
                            best_op = ('remove', i, j)
                        adj[i, j] = 1

                    # Try reversing edge i → j to j → i
                    if adj[i, j] == 1 and (j, i) not in bl_idx:
                        adj[i, j] = 0
                        adj[j, i] = 1
                        if is_dag(adj):
                            new_score = bic_score_dag(data, adj, variables)
                            delta = new_score - current_score
                            if delta > best_delta:
                                best_delta = delta
                                best_op = ('reverse', i, j)
                        adj[j, i] = 0
                        adj[i, j] = 1

            if best_op is not None:
                op, i, j = best_op
                if op == 'add':
                    adj[i, j] = 1
                elif op == 'remove':
                    adj[i, j] = 0
                elif op == 'reverse':
                    adj[i, j] = 0
                    adj[j, i] = 1
                current_score += best_delta
                improved = True

        if current_score > best_global_score:
            best_global_adj = adj.copy()
            best_global_score = current_score

    return best_global_adj, best_global_score


# ════════════════════════════════════════════════════════════════════
# PC ALGORITHM
# ════════════════════════════════════════════════════════════════════

def pc_algorithm(data: pd.DataFrame, variables: list,
                 alpha: float = 0.05, max_cond_size: int = None) -> tuple:
    """
    PC algorithm for causal discovery.
    Returns (directed_adj, skeleton_adj, separation_sets).
    """
    n_vars = len(variables)
    if max_cond_size is None:
        max_cond_size = n_vars - 2

    # Phase 1: Build skeleton via conditional independence tests
    skeleton = np.ones((n_vars, n_vars), dtype=int)
    np.fill_diagonal(skeleton, 0)
    sep_sets = {}

    for cond_size in range(max_cond_size + 1):
        edges_to_test = []
        for i in range(n_vars):
            for j in range(i + 1, n_vars):
                if skeleton[i, j] == 1:
                    edges_to_test.append((i, j))

        for i, j in edges_to_test:
            if skeleton[i, j] == 0:
                continue

            adj_i = [k for k in range(n_vars) if skeleton[i, k] == 1 and k != j]
            adj_j = [k for k in range(n_vars) if skeleton[j, k] == 1 and k != i]
            candidates = list(set(adj_i + adj_j))

            if len(candidates) < cond_size:
                continue

            for cond_set_indices in combinations(candidates, cond_size):
                cond_set = [variables[k] for k in cond_set_indices]
                _, p_value, _ = chi_square_test(data, variables[i], variables[j], cond_set)
                if p_value > alpha:
                    skeleton[i, j] = 0
                    skeleton[j, i] = 0
                    sep_sets[(i, j)] = set(cond_set_indices)
                    sep_sets[(j, i)] = set(cond_set_indices)
                    break

    # Phase 2: Orient edges (v-structures)
    directed = skeleton.copy()
    for j in range(n_vars):
        parents = [i for i in range(n_vars) if directed[i, j] == 1]
        for a, b in combinations(parents, 2):
            if directed[a, b] == 0 and directed[b, a] == 0:
                if (j not in sep_sets.get((a, b), set()) and
                        j not in sep_sets.get((b, a), set())):
                    directed[j, a] = 0
                    directed[j, b] = 0

    return directed, skeleton, sep_sets


# ════════════════════════════════════════════════════════════════════
# EDGE ANALYSIS
# ════════════════════════════════════════════════════════════════════

def compute_edge_pvalues(data: pd.DataFrame, adj_matrix: np.ndarray,
                         variables: list) -> pd.DataFrame:
    """Compute chi-square p-values and MI for all edges in a DAG."""
    edges = []
    for i in range(len(variables)):
        for j in range(len(variables)):
            if adj_matrix[i, j] > 0:
                chi2, pval, dof = chi_square_test(data, variables[i], variables[j])
                mi = mutual_information(data, variables[i], variables[j])
                edges.append({
                    'source': variables[i],
                    'target': variables[j],
                    'chi2': round(chi2, 2),
                    'pvalue': pval,
                    'neg_log10_pval': round(-np.log10(max(pval, 1e-20)), 2),
                    'mutual_info': round(mi, 4),
                    'dof': dof,
                })
    return pd.DataFrame(edges)


# ════════════════════════════════════════════════════════════════════
# BOOTSTRAP STABILITY
# ════════════════════════════════════════════════════════════════════

def bootstrap_structure(data: pd.DataFrame, variables: list,
                        n_bootstrap: int = 30, method: str = 'hillclimb',
                        max_parents: int = 3, blacklist: set = None,
                        alpha: float = 0.05,
                        progress_callback=None) -> np.ndarray:
    """
    Bootstrap resampling for edge stability.
    Returns edge frequency matrix (n_vars × n_vars).
    """
    n_vars = len(variables)
    edge_counts = np.zeros((n_vars, n_vars))
    n = len(data)

    for b in range(n_bootstrap):
        if progress_callback and (b + 1) % 10 == 0:
            progress_callback(b + 1, n_bootstrap)

        sample = data.sample(n=n, replace=True).reset_index(drop=True)

        if method == 'hillclimb':
            adj, _ = hillclimb_search(sample, variables,
                                       max_parents=max_parents,
                                       restarts=1, blacklist=blacklist)
        else:
            adj, _, _ = pc_algorithm(sample, variables, alpha=alpha)

        edge_counts += (adj > 0).astype(int)

    return edge_counts / n_bootstrap


# ════════════════════════════════════════════════════════════════════
# VISUALIZATION
# ════════════════════════════════════════════════════════════════════

def plot_dag(adj_matrix: np.ndarray, variables: list, config: dict,
             title: str = "Causal DAG", filename: str = "dag.png") -> str:
    """Plot a DAG using matplotlib with circular layout. Returns filepath."""
    n = len(variables)
    bg = config.get('bg_dark', '#1a1a2e')
    text_color = config.get('text_light', '#e9ecef')
    purple = config.get('primary_purple', '#6f42c1')
    accent = config.get('accent_colors', {})
    out_dir = config.get('output_dir', '.')
    figsize = config.get('figsize', (14, 10))

    fig, ax = plt.subplots(1, 1, figsize=figsize, facecolor=bg)
    ax.set_facecolor(bg)

    angles = np.linspace(0, 2 * np.pi, n, endpoint=False) - np.pi / 2
    radius = 3.5
    positions = {variables[i]: (radius * np.cos(angles[i]),
                                radius * np.sin(angles[i])) for i in range(n)}

    def get_color(var_name):
        for key, color in accent.items():
            if key in var_name.lower():
                return color
        return accent.get('default', '#a0a0c0')

    # Draw edges
    for i in range(n):
        for j in range(n):
            val = adj_matrix[i, j]
            if val > 0:
                x1, y1 = positions[variables[i]]
                x2, y2 = positions[variables[j]]
                weight = val if isinstance(val, float) and val <= 1.0 else 1.0
                alpha_val = max(0.3, min(1.0, weight))
                lw = 1.0 + 2.0 * weight

                dx, dy = x2 - x1, y2 - y1
                dist = math.sqrt(dx**2 + dy**2)
                if dist == 0:
                    continue
                shrink = 0.45
                ax.annotate('', xy=(x2 - dx * shrink / dist, y2 - dy * shrink / dist),
                            xytext=(x1 + dx * shrink / dist, y1 + dy * shrink / dist),
                            arrowprops=dict(arrowstyle='->', color=purple,
                                           lw=lw, alpha=alpha_val,
                                           connectionstyle='arc3,rad=0.1'))

                if isinstance(val, float) and val < 1.0:
                    mid_x = (x1 + x2) / 2 + 0.15
                    mid_y = (y1 + y2) / 2 + 0.15
                    ax.text(mid_x, mid_y, f'{val:.0%}', fontsize=7,
                            color=text_color, alpha=0.7, ha='center')

    # Draw nodes
    for var in variables:
        x, y = positions[var]
        color = get_color(var)
        circle = plt.Circle((x, y), 0.4, color=color, ec='white',
                            linewidth=1.5, zorder=5)
        ax.add_patch(circle)
        label = var.replace('_', '\n')
        ax.text(x, y, label, ha='center', va='center', fontsize=8,
                fontweight='bold', color='white', zorder=6)

    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=16, fontweight='bold', color='white', pad=20)

    filepath = os.path.join(out_dir, filename)
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor=bg)
    plt.close()
    return filepath


def plot_bootstrap_heatmap(boot_freq: np.ndarray, variables: list,
                           config: dict) -> str:
    """Plot bootstrap edge frequency heatmap. Returns filepath."""
    bg = config.get('bg_dark', '#1a1a2e')
    text_color = config.get('text_light', '#e9ecef')
    purple = config.get('primary_purple', '#6f42c1')
    out_dir = config.get('output_dir', '.')

    fig, ax = plt.subplots(figsize=(12, 10), facecolor=bg)
    ax.set_facecolor(bg)

    from matplotlib.colors import LinearSegmentedColormap
    colors_list = [bg, '#2d1b4e', '#4a2d7a', purple, '#b088e0', '#e0d0f0']
    cmap = LinearSegmentedColormap.from_list('kearney', colors_list, N=256)

    short_labels = [v[:12] for v in variables]
    im = ax.imshow(boot_freq, cmap=cmap, vmin=0, vmax=1, aspect='equal')

    ax.set_xticks(range(len(variables)))
    ax.set_yticks(range(len(variables)))
    ax.set_xticklabels(short_labels, rotation=45, ha='right', fontsize=9, color=text_color)
    ax.set_yticklabels(short_labels, fontsize=9, color=text_color)

    for i in range(len(variables)):
        for j in range(len(variables)):
            val = boot_freq[i, j]
            if val > 0.05:
                ax.text(j, i, f'{val:.0%}', ha='center', va='center',
                        fontsize=8, fontweight='bold',
                        color='white' if val > 0.4 else text_color)

    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('Bootstrap Edge Frequency', color=text_color, fontsize=11)
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color=text_color)

    ax.set_xlabel('Target (Child)', fontsize=11, color=text_color)
    ax.set_ylabel('Source (Parent)', fontsize=11, color=text_color)
    ax.set_title('Causal Edge Bootstrap Stability\n(rows → columns)',
                 fontsize=14, fontweight='bold', color='#FFFFFF')

    filepath = os.path.join(out_dir, 'bootstrap_heatmap.png')
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor=bg)
    plt.close()
    return filepath


def plot_edge_confidence(edge_df: pd.DataFrame, config: dict) -> str:
    """Plot edge confidence bar chart. Returns filepath."""
    bg = config.get('bg_dark', '#1a1a2e')
    text_color = config.get('text_light', '#e9ecef')
    purple = config.get('primary_purple', '#6f42c1')
    green_thresh = config.get('green_threshold', 0.70)
    out_dir = config.get('output_dir', '.')

    df = edge_df.sort_values('bootstrap_freq', ascending=True)
    labels = [f"{r['source']} → {r['target']}" for _, r in df.iterrows()]
    freqs = df['bootstrap_freq'].values

    fig, ax = plt.subplots(figsize=(12, max(6, len(labels) * 0.35)), facecolor=bg)
    ax.set_facecolor(bg)

    colors = [purple if f >= green_thresh else '#8a6dba' for f in freqs]
    ax.barh(range(len(labels)), freqs, color=colors, edgecolor='none', height=0.7)

    ax.axvline(x=green_thresh, color='#4ade80', linestyle='--', alpha=0.5, linewidth=1)
    ax.axvline(x=0.5, color='#facc15', linestyle='--', alpha=0.3, linewidth=1)

    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=8, color=text_color)
    ax.set_xlabel('Bootstrap Frequency', color=text_color, fontsize=11)
    ax.set_title('Edge Confidence (Bootstrap Resamples)',
                 fontsize=14, fontweight='bold', color='white')
    ax.tick_params(colors=text_color)
    for spine in ax.spines.values():
        spine.set_color('#333355')

    ax.legend([f'High confidence ({green_thresh:.0%})',
               f'Moderate confidence (50%)'],
              loc='lower right', fontsize=8,
              facecolor=bg, edgecolor='#333355', labelcolor=text_color)

    filepath = os.path.join(out_dir, 'edge_confidence.png')
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor=bg)
    plt.close()
    return filepath


# ════════════════════════════════════════════════════════════════════
# MAIN ENGINE CLASS
# ════════════════════════════════════════════════════════════════════

class CausalDiscoveryEngine:
    """
    Self-contained Bayesian causal discovery engine.

    Usage:
        config = {
            'target_variable': 'revenue_growth',
            'exogenous_variables': ['weather', 'macro_index'],
            'output_dir': './results',
        }
        engine = CausalDiscoveryEngine(config)
        results = engine.run(df)
    """

    def __init__(self, config: dict = None):
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        os.makedirs(self.config['output_dir'], exist_ok=True)

    def _log(self, msg: str):
        print(msg)

    def discretize(self, df: pd.DataFrame) -> pd.DataFrame:
        """Discretize continuous variables into quantile bins."""
        n_bins = self.config['n_bins']
        labels = self.config['bin_labels']
        if labels is None:
            if n_bins == 2:
                labels = [0, 1]
            elif n_bins == 3:
                labels = [0, 1, 2]
            elif n_bins == 4:
                labels = [0, 1, 2, 3]
            else:
                labels = list(range(n_bins))

        disc = pd.DataFrame(index=df.index)
        for col in df.columns:
            try:
                disc[col] = pd.qcut(df[col], q=n_bins, labels=labels,
                                     duplicates='drop').astype(int)
            except (ValueError, TypeError):
                disc[col] = pd.cut(df[col], bins=n_bins, labels=labels[:n_bins],
                                    duplicates='drop').astype(int)
        return disc.dropna()

    def _build_blacklist(self, variables: list) -> set:
        """Build blacklist from config: exogenous + explicit + target constraints."""
        blacklist = set()
        target = self.config['target_variable']

        # Target cannot cause features (it's a future outcome)
        if target and target in variables:
            for v in variables:
                if v != target:
                    blacklist.add((target, v))

        # Exogenous variables cannot be caused by endogenous variables
        exog = set(self.config['exogenous_variables'])
        endog = [v for v in variables if v not in exog and v != target]
        for ex in exog:
            if ex in variables:
                for en in endog:
                    if en in variables:
                        blacklist.add((en, ex))

        # Explicit blacklist
        for src, tgt in self.config.get('blacklist', []):
            if src in variables and tgt in variables:
                blacklist.add((src, tgt))

        return blacklist

    def run(self, df: pd.DataFrame) -> dict:
        """
        Run the full causal discovery pipeline.

        Args:
            df: DataFrame with columns as variables (can be continuous or discrete).
                Must include the target variable if specified in config.

        Returns:
            dict with keys: metadata, hillclimb, pc, agreement, bootstrap, confidence_table
        """
        np.random.seed(42)
        cfg = self.config

        self._log("=" * 70)
        self._log("BAYESIAN CAUSAL DISCOVERY ENGINE")
        self._log("=" * 70)

        # --- Validate ---
        variables = list(df.columns)
        target = cfg['target_variable']
        if target and target not in variables:
            raise ValueError(f"Target variable '{target}' not found in DataFrame columns: {variables}")

        self._log(f"\n[1/6] Input: {df.shape[0]} rows × {df.shape[1]} variables")
        self._log(f"  Variables: {variables}")
        if target:
            self._log(f"  Target: {target}")

        # --- Discretize ---
        self._log(f"\n[2/6] Discretizing ({cfg['n_bins']} bins)...")
        disc_data = self.discretize(df)
        variables = list(disc_data.columns)
        self._log(f"  After discretization: {disc_data.shape[0]} rows × {disc_data.shape[1]} vars")

        # --- Blacklist ---
        blacklist = self._build_blacklist(variables)
        self._log(f"  Blacklist: {len(blacklist)} forbidden edges")

        # --- HillClimb ---
        self._log(f"\n[3/6] HillClimb structure learning (BIC, {cfg['hc_restarts']} restarts)...")
        hc_adj, hc_score = hillclimb_search(
            disc_data, variables,
            max_parents=cfg['hc_max_parents'],
            restarts=cfg['hc_restarts'],
            blacklist=blacklist
        )
        hc_edges_df = compute_edge_pvalues(disc_data, hc_adj, variables)
        self._log(f"  BIC score: {hc_score:.1f}")
        self._log(f"  Edges found: {int(hc_adj.sum())}")
        if not hc_edges_df.empty:
            for _, row in hc_edges_df.iterrows():
                sig = '***' if row['pvalue'] < 0.001 else ('**' if row['pvalue'] < 0.01 else ('*' if row['pvalue'] < 0.05 else ''))
                self._log(f"    {row['source']:>25} → {row['target']:<25} chi2={row['chi2']:>7.1f}  p={row['pvalue']:.4f} {sig}")

        # --- PC algorithm ---
        self._log(f"\n[4/6] PC algorithm (α={cfg['pc_alpha']})...")
        pc_adj, pc_skeleton, pc_sep = pc_algorithm(
            disc_data, variables,
            alpha=cfg['pc_alpha'],
            max_cond_size=cfg.get('pc_max_cond_size')
        )
        pc_edges_df = compute_edge_pvalues(disc_data, pc_adj, variables)
        self._log(f"  Edges found: {int((pc_adj > 0).sum())}")

        # --- Method agreement ---
        hc_set = {(variables[i], variables[j])
                  for i in range(len(variables)) for j in range(len(variables))
                  if hc_adj[i, j] == 1}
        pc_set = {(variables[i], variables[j])
                  for i in range(len(variables)) for j in range(len(variables))
                  if pc_adj[i, j] == 1}
        agreed = hc_set & pc_set
        hc_only = hc_set - pc_set
        pc_only = pc_set - hc_set

        self._log(f"\n  Method agreement:")
        self._log(f"    Both: {len(agreed)} edges")
        for e in sorted(agreed):
            self._log(f"      ✓ {e[0]} → {e[1]}")
        self._log(f"    HillClimb only: {len(hc_only)}")
        self._log(f"    PC only: {len(pc_only)}")

        # --- Bootstrap ---
        self._log(f"\n[5/6] Bootstrap stability ({cfg['n_bootstrap']} resamples)...")
        boot_freq = bootstrap_structure(
            disc_data, variables,
            n_bootstrap=cfg['n_bootstrap'],
            method=cfg['bootstrap_method'],
            max_parents=cfg['hc_max_parents'],
            blacklist=blacklist,
            alpha=cfg['pc_alpha'],
            progress_callback=lambda b, t: self._log(f"  Bootstrap {b}/{t}")
        )

        # Build confidence table
        green_t = cfg['green_threshold']
        yellow_t = cfg['yellow_threshold']
        min_freq = cfg['min_report_freq']

        boot_edges = []
        for i in range(len(variables)):
            for j in range(len(variables)):
                freq = boot_freq[i, j]
                if freq > min_freq:
                    in_hc = (variables[i], variables[j]) in hc_set
                    in_pc = (variables[i], variables[j]) in pc_set
                    method_count = int(in_hc) + int(in_pc)
                    chi2, pval, _ = chi_square_test(disc_data, variables[i], variables[j])
                    mi = mutual_information(disc_data, variables[i], variables[j])

                    if freq >= green_t and method_count >= 2:
                        tier = 'GREEN'
                    elif freq >= yellow_t or method_count >= 1:
                        tier = 'YELLOW'
                    else:
                        tier = 'RED'

                    boot_edges.append({
                        'source': variables[i],
                        'target': variables[j],
                        'bootstrap_freq': round(freq, 3),
                        'in_hillclimb': in_hc,
                        'in_pc': in_pc,
                        'method_agreement': method_count,
                        'chi2': round(chi2, 2),
                        'pvalue': pval,
                        'mutual_info': round(mi, 4),
                        'confidence_tier': tier,
                    })

        boot_edge_df = pd.DataFrame(boot_edges).sort_values('bootstrap_freq', ascending=False)

        self._log(f"\n  Confidence table ({len(boot_edge_df)} edges):")
        self._log(f"  {'Source':>25} → {'Target':<25} {'Freq':>6} {'HC':>3} {'PC':>3} {'Tier':>6}")
        self._log("  " + "-" * 80)
        for _, row in boot_edge_df.iterrows():
            hc_mark = '✓' if row['in_hillclimb'] else ' '
            pc_mark = '✓' if row['in_pc'] else ' '
            self._log(f"  {row['source']:>25} → {row['target']:<25} "
                      f"{row['bootstrap_freq']:>5.0%}  {hc_mark:>2}  {pc_mark:>2}  "
                      f"{row['confidence_tier']:>6}")

        # --- Visualizations ---
        plots = []
        if cfg.get('save_plots', True):
            self._log(f"\n[6/6] Generating visualizations...")
            plots.append(plot_dag(hc_adj, variables, cfg,
                                  title="HillClimb DAG (BIC Scoring)",
                                  filename="dag_hillclimb.png"))
            plots.append(plot_dag(pc_adj, variables, cfg,
                                  title=f"PC Algorithm DAG (α={cfg['pc_alpha']})",
                                  filename="dag_pc.png"))
            conf_adj = boot_freq.copy()
            conf_adj[conf_adj < yellow_t] = 0
            plots.append(plot_dag(conf_adj, variables, cfg,
                                  title=f"Bootstrap Confidence DAG (>{yellow_t:.0%} frequency)",
                                  filename="dag_bootstrap.png"))
            plots.append(plot_bootstrap_heatmap(boot_freq, variables, cfg))
            if not boot_edge_df.empty:
                plots.append(plot_edge_confidence(boot_edge_df, cfg))
            self._log(f"  Saved {len(plots)} plots to {cfg['output_dir']}/")

        # --- Assemble results ---
        results = {
            'metadata': {
                'engine': 'bayesian-causal-discovery',
                'version': '1.0.0',
                'observations': int(disc_data.shape[0]),
                'variables': variables,
                'target': target,
                'exogenous': list(cfg['exogenous_variables']),
                'discretization': f"{cfg['n_bins']}-bin quantile",
                'blacklist_size': len(blacklist),
            },
            'hillclimb': {
                'bic_score': round(hc_score, 2),
                'restarts': cfg['hc_restarts'],
                'edges': hc_edges_df.to_dict('records') if not hc_edges_df.empty else [],
            },
            'pc': {
                'alpha': cfg['pc_alpha'],
                'edges': pc_edges_df.to_dict('records') if not pc_edges_df.empty else [],
            },
            'agreement': {
                'both': [list(e) for e in sorted(agreed)],
                'hillclimb_only': [list(e) for e in sorted(hc_only)],
                'pc_only': [list(e) for e in sorted(pc_only)],
            },
            'bootstrap': {
                'n_resamples': cfg['n_bootstrap'],
                'method': cfg['bootstrap_method'],
                'edges': boot_edge_df.to_dict('records') if not boot_edge_df.empty else [],
            },
            'confidence_summary': {
                'green': len(boot_edge_df[boot_edge_df['confidence_tier'] == 'GREEN']) if not boot_edge_df.empty else 0,
                'yellow': len(boot_edge_df[boot_edge_df['confidence_tier'] == 'YELLOW']) if not boot_edge_df.empty else 0,
                'red': len(boot_edge_df[boot_edge_df['confidence_tier'] == 'RED']) if not boot_edge_df.empty else 0,
            },
            'plots': plots,
        }

        # Save outputs
        out = cfg['output_dir']
        with open(os.path.join(out, 'causal_discovery_results.json'), 'w') as f:
            json.dump(results, f, indent=2, default=str)
        if not boot_edge_df.empty:
            boot_edge_df.to_csv(os.path.join(out, 'edge_confidence_table.csv'), index=False)

        self._log(f"\n{'='*70}")
        self._log(f"DONE — {results['confidence_summary']['green']} GREEN, "
                  f"{results['confidence_summary']['yellow']} YELLOW, "
                  f"{results['confidence_summary']['red']} RED edges")
        self._log(f"Results: {out}/causal_discovery_results.json")
        self._log(f"{'='*70}")

        return results


# ════════════════════════════════════════════════════════════════════
# CLI ENTRYPOINT
# ════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python engine.py <data.csv> [--target TARGET] [--exog COL1,COL2]")
        print("       python engine.py <data.csv> --target revenue --exog weather,macro --bins 3")
        sys.exit(1)

    data_path = sys.argv[1]
    config = {}

    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == '--target' and i + 1 < len(args):
            config['target_variable'] = args[i + 1]
            i += 2
        elif args[i] == '--exog' and i + 1 < len(args):
            config['exogenous_variables'] = args[i + 1].split(',')
            i += 2
        elif args[i] == '--bins' and i + 1 < len(args):
            config['n_bins'] = int(args[i + 1])
            i += 2
        elif args[i] == '--output' and i + 1 < len(args):
            config['output_dir'] = args[i + 1]
            i += 2
        elif args[i] == '--bootstrap' and i + 1 < len(args):
            config['n_bootstrap'] = int(args[i + 1])
            i += 2
        else:
            i += 1

    df = pd.read_csv(data_path)
    engine = CausalDiscoveryEngine(config)
    engine.run(df)
