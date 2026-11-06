# System Blueprint (_a.k.a._ "Design Doc")

## TNPG: Hypergamy
## project: WeBlog
## Target ship date: {2026-11-20}

---

#### roster:


| Name | Email | Primary Role | Secondary Role |
| Leon Wong | leonw17@nycstudents.net |---|---|
| Marcos Lehman | marcosl30@nycstudents.net |---|---|
| Wenjie Ma | wenjiem@nycstudents.net |---|---|
| Efrat Hossain | efrath3@nycstudents.net |---|---|

---


# Summary
Super awesome blog hosting and sharing site, where you can update your own blog and see blogs of other users.

## Problem Being Solved
Have you ever wanted to have blog posts 'n' stuff, but don't want to pay ten thousands of $$$ to the tech overlords to get it? Well now there is one, for free! (we're not the ones paying for it lol)

## Target Users

Who will use this system?

- People who want blog posts
- People who want to look at them
- ~~Sam Altman's web crawlers~~


## Why This Project Matters
If we make it, we get good experience for teamworking and making a project. ~~also we get a good grade in the class~~

---

# Minimum Viable Product (MVP) Scope

## Core Features (Required for Final Submission)
Features that **must** be completed:
1. Login/logout/storing info on accounts in databases
1. Seeing the blog posts of a specific user
1. A way to edit your blog posts.
1. Seeing all your unpublished / published blog posts, and being able to publish/unpublish them.

## Stretch Features (Only if MVP is Complete)
1. A main feed that shows blog posts from multiple users (these are just the most recently published ones)
1. 
1. 

## Explicit Non-Goals
- 
- 

Features intentionally excluded:
- 
- 

---

# Technology Stack

| Layer | Selected Tool |
|---|---|
| Backend Framework | Flask |
| Frontend Framework | none |
| Database | SQLite |
| Authentication | Flask sessions  |

## Why This Stack Was Chosen
This section and the one above it fixed/given for Project0

---

# Team Ownership Plan

Each member must own meaningful deliverables.

| Team Member | Primary Ownership | Secondary Ownership | Specific Deliverables |
|---|---|---|---|
| Marcos | Databases | Backend | Login System, Storing Blog Posts |
| Wenjie | Webpage Design | Backend | Create webpages design |
| Leon | Webpage Design | Databases | Create webpages design |
| Efrat | Backend | Databases | Routing routes |

---

# Component map

``` mermaid
flowchart TD
    A(Website Interface)<-->B("Flask server (app.py)")
    B<-->Backend
    Backend<-->F("Database management (SQLite3 queries)")
    F<-->G(Database)

subgraph Backend
    C("Authentication (auth.py)")
    D("Page Management (blog_view.py)")
    E("Search Engine (search.py)")
end
```

# Site map

``` mermaid
flowchart TD
    Start[START]-->Home[home.html]
    Home-->|pressed login?|Login[login.html]
    Login-->LoginD{Correct credentials?}
    LoginD-->|true|LoginT(Add user to session)-->Home
    LoginD-->|false|LoginF(Redirect, show error message on the page)-->Login

    Home-->|pressed sign up?|NewUser[new_user.html]
    NewUser-->NewUserD{Username taken?}
    NewUserD-->|true|NewUserT(Redirect, show error message on the page)-->NewUser
    NewUserD-->|false|NewUserF(Add account info to DB)-->NewUserF2(Add user to session)-->Home

    Home-->|pressed Profile?|z(Redirect to blog_view, but with your own id as the page you are viewing)
    z-->Stranger
    Stranger-->|"pressed edit? (edit button does not appear unless you made the post)"|Edit[blog_edit.html]
    Edit-->|pressed save and exit?|Stranger

    Home-->|Searched for a username?|Search[search.html]
    Search-->|pressed home?|Home
    Search-->|clicked a user?|Stranger[blog_view.html]
    Stranger-->|clicked home?|Home
```

## Key User Stories
### eg0
As a __________, I want to __________ so that...

### eg1
As a __________, I want to __________ so that...

### eg2
As a __________, I want to __________ so that...



# Database Design

{Insert your table/document organizational structure here. See N&C for schema representation conventions.}


# Testing Plan
{Delineate here your plan for testing each component}

# Timeline
## day0 Goals:
## ...
## dayX Goals:
## Internal Deadlines:
{List milestones your team has identified, in the order they must be completed. Set a target completion date for each.}


# Completion Criteria (_a.k.a._ "Definition of 'Done'")
Project is considered complete when all of the following are true:
1.
1.
1.

# Open Questions
{Delineate anything undecided here}

# Appendix
{Any relevant info that is useful but would have interrupted narrative flow above, or cluttered the information portrayed}

# Other
{Put here anything that did not sensibly fit under above headings. This section will inform evolution of SoftDev.}
