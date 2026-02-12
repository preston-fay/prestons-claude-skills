---
name: interview
description: "Conversational requirements gathering for any project. Use when starting a new engagement, feature, or analysis to systematically capture objectives, constraints, stakeholders, and success criteria through structured dialogue."
disable-model-invocation: true
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Glob
hooks:
  PostToolUse:
    - matcher: Write
      command: ["bash", "/Users/pfay01/.claude/hooks/log-tool-use.sh"]
---

# Requirements Interview

Structured conversational approach to gather complete requirements for any project type. Ask questions ONE AT A TIME and adapt based on responses.

## Interview Framework

### Phase 1: Context & Objectives

**Start here. Ask these questions one at a time, waiting for each response.**

1. **The Opener**
   "Tell me about the project/problem in your own words. What are we trying to accomplish?"

2. **The Why**
   "What's driving this work? Is there a business problem, opportunity, or event that triggered it?"

3. **Success Definition**
   "If this project is wildly successful, what does that look like? How would you measure it?"

4. **Stakeholders**
   "Who are the key stakeholders? Who will use the output? Who needs to approve it?"

### Phase 2: Scope & Constraints

5. **Boundaries**
   "What's explicitly IN scope? What's OUT of scope?"

6. **Timeline**
   "What are the key dates or deadlines? Are there hard deadlines vs. preferred timelines?"

7. **Resources**
   "What resources are available? (Data, budget, team, tools, access)"

8. **Constraints**
   "What constraints should I know about? (Technical, political, regulatory, budget)"

### Phase 3: Requirements Deep-Dive

**Adapt these based on project type:**

#### For Data/Analytics Projects

9. "What data sources are available? Where does the data live?"

10. "What questions need to be answered? What decisions will this inform?"

11. "Who is the audience for the analysis? What's their data literacy?"

12. "What format should the output take? (Dashboard, report, presentation, model)"

#### For Application/Feature Projects

9. "Who are the users? What are their roles and goals?"

10. "What are the key user journeys or workflows?"

11. "What systems need to integrate? What's the technical environment?"

12. "What are the security/compliance requirements?"

#### For Strategy/Consulting Projects

9. "What's the current state? What's been tried before?"

10. "Who are the key decision-makers? What's the approval process?"

11. "What's the expected deliverable format?"

12. "Are there political sensitivities or change management concerns?"

### Phase 4: Priorities & Risks

13. **Prioritization**
    "If we can't do everything, what's most important? What's nice-to-have?"

14. **Risks**
    "What could go wrong? What are you most worried about?"

15. **Dependencies**
    "What does this project depend on? What depends on this project?"

### Phase 5: Confirmation

16. **Summary Check**
    "Let me summarize what I've heard... [provide summary]. Did I capture this correctly?"

17. **Missing Pieces**
    "Is there anything important we haven't discussed?"

18. **Next Steps**
    "What should happen next? Who needs to do what?"

---

## Output: Requirements Document

After the interview, generate a structured requirements document:

```markdown
# Project Requirements

## Executive Summary
[2-3 sentence overview of the project]

## Objectives
### Primary Objective
[Clear statement of the main goal]

### Success Criteria
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]
- [ ] [Measurable criterion 3]

## Stakeholders
| Role | Name | Responsibility |
|------|------|----------------|
| Sponsor | [Name] | Final approval |
| Owner | [Name] | Day-to-day decisions |
| Users | [Group] | End users of output |

## Scope

### In Scope
- [Item 1]
- [Item 2]

### Out of Scope
- [Item 1]
- [Item 2]

### Assumptions
- [Assumption 1]
- [Assumption 2]

## Requirements

### Functional Requirements
1. [Requirement 1]
2. [Requirement 2]

### Non-Functional Requirements
1. [Performance, security, etc.]

### Data Requirements
- Sources: [List data sources]
- Access: [How to access]
- Quality concerns: [Known issues]

## Constraints
- Timeline: [Key dates]
- Budget: [If applicable]
- Technical: [Limitations]
- Other: [Political, regulatory, etc.]

## Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Strategy] |

## Priorities (MoSCoW)
### Must Have
- [Critical items]

### Should Have
- [Important but not critical]

### Could Have
- [Nice to have]

### Won't Have (this phase)
- [Explicitly excluded]

## Timeline
| Milestone | Date | Owner |
|-----------|------|-------|
| [Milestone 1] | [Date] | [Name] |

## Next Steps
1. [Immediate action 1]
2. [Immediate action 2]

---
*Captured: [Date]*
*Interviewer: Claude*
*Interviewee: [Name/Role]*
```

---

## Interview Tips

### Techniques

1. **Active Listening**: Reflect back what you heard before moving on
2. **5 Whys**: When something seems important, ask "why?" up to 5 times
3. **Concrete Examples**: "Can you give me an example of that?"
4. **Worst Case**: "What happens if we don't do this?"
5. **Best Case**: "In a perfect world, what would this look like?"

### Red Flags to Probe

- Vague success criteria ("make it better")
- Unclear ownership ("we all decide together")
- Missing constraints ("no deadline, just ASAP")
- Scope creep signals ("while we're at it...")
- Conflicting requirements between stakeholders

### Handling Common Situations

**"I don't know"**
→ "Who would know? Can we get them involved?"
→ "What's your best guess? We can validate later."

**Conflicting requirements**
→ "I'm hearing X from you and Y from [other stakeholder]. How should we reconcile that?"
→ Document both and flag for resolution

**Scope creep**
→ "That's a great idea. Should we add it to the current scope or capture it for a future phase?"

**Unrealistic timeline**
→ "To hit that date, what could we cut or simplify?"
→ "What's driving that date? Is there flexibility?"

---

## Quick Interview Modes

### 5-Minute Quick Capture
For small requests or clarifications:
1. What do you need?
2. When do you need it?
3. What format?
4. Anything else I should know?

### 15-Minute Feature Request
1. What's the problem/opportunity?
2. Who's affected?
3. What does success look like?
4. What are the constraints?
5. What's the priority?

### 30-Minute Project Kickoff
Full Phase 1-3 above, abbreviated Phase 4-5

### 60-Minute Comprehensive
Full interview framework with deep-dives

---

## Conversation Starters by Domain

### Analytics/Data Science
- "What decisions will this analysis inform?"
- "What would you do differently if you knew X?"
- "How is this done today without the analysis?"

### Product/Features
- "Walk me through a day in the life of your user"
- "What's the most painful part of the current process?"
- "How do competitors solve this?"

### Strategy/Consulting
- "What's changed that makes this important now?"
- "What's the hypothesis you're testing?"
- "Who needs to be convinced?"

### Operations/Process
- "How long does this take today?"
- "Where do things typically go wrong?"
- "What would 10x improvement look like?"
