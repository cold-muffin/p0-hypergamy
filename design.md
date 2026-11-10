# System Blueprint (_a.k.a._ "Design Doc")

## TNPG: Hypergamy
## project: WeBlog
## Target ship date: {2026-11-18}

---

#### roster:


| Name | Email | Primary Role | Secondary Role |
|---|---|---|---|
| Leon Wong | leonw17@nycstudents.net | Databases | Backend |
| Marcos Lehman | marcosl30@nycstudents.net | Webpage Design | Backend |
| Wenjie Ma | wenjiem@nycstudents.net | Webpage Design | Databases |
| Efrat Hossain | efrath3@nycstudents.net | Backend | Databases |

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
1. No edit or create button appearing on posts that aren't yours. (The buttons won't work on posts you don't own anyways)
1. Let users create a bio, maybe even a profile image?
1. Super stretch: A main feed that shows blog posts from multiple users (these are just the most recently published ones)

## Explicit Non-Goals
- Live rendering of the html text as you edit it.

Features intentionally excluded:
- View counter. It's too hard for many reasons.

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
    Start[START]-->Home["/"]
    Home-->|pressed login|Login["/login"]
    Login-->LoginD{Correct credentials?}
    LoginD-->|true|LoginT(Add user to session)-->Home
    LoginD-->|false|LoginF(Redirect, show error message on the page)-->Login

    Home-->|pressed sign up|NewUser["/new_user"]
    NewUser-->NewUserD{Username taken?}
    NewUserD-->|true|NewUserT(Redirect, show error message on the page)-->NewUser
    NewUserD-->|false|NewUserF(Add account info to DB)-->NewUserF2(Add user to session)-->Home

    Home-->|pressed search|Search("/search")
    Search-->SearchD{Query matches exactly with an existing user?}
    SearchD-->|true|ProfilesUID("/profiles/{user_id}")
    SearchD-->|false|ProfilesF("/search?match=false, and show a list of all partial matches")
    ProfilesF-->|"click option"|ProfilesUID

    ProfilesUID-->|pressed edit|EditD{post_owner is logged in user?}
    EditD-->|true|Editable("/profiles/{user_id}/edit/{post_id}")
    EditD-->|false|EditPermDenied("/profiles/{user_id}/edit/permission_denied")-->ProfilesUID

    ProfilesUID-->|pressed create|CreateD{post_owner is logged in user?}
    CreateD-->|true|Editable
    CreateD-->|false|EditPermDenied

    Editable-->|pressed cancel|ProfilesUID
    Editable-->|pressed save|ATDB("add/edit to DB")-->Editable
    Editable-->|pressed save and exit|ATDB2("add/edit to DB")-->ProfilesUID
```

## Key User Stories
### eg0
As a writer, I want to make the blog posts so that people think I'm supa cool.

### eg1
As a person, I want to read other people's blog posts so that I can get dopamine.

### eg2
As a web crawler, I want to eat all the blog posts so that I can make my masters rich.



# Database Design

```mermaid
erDiagram
    users {
        INTEGER uuid "PK, AUTOINCREMENT"
        TEXT username
        BLOB password
    }
```

```mermaid
erDiagram
    blog_posts {
        INTEGER pid "PK, AUTOINCREMENT"
        INTEGER owner
        TEXT title
        BLOB contents
        INTEGER published
    }
```

### Example of populated DBs
users
|uuid INTEGER PRIMARY KEY|username TEXT|password BLOB|
|---|---|---|
|1|coldmuffin|\(hashed password\)|
|2|john_doe_|\(hashed password\)|
|3|jawed|\(hashed password\)|

blog_posts
|pid INTEGER PRIMARY KEY AUTOINCREMENT|owner INTEGER|title TEXT|contents BLOB|published INTEGER|
|---|---|---|---|---|
|1|3|Going to the zoo today!|\(the html file of the blog post\)|1|
|2|2|Generic Manifesto|\(the html file of the blog post\)|0|
|3|2|Looking for Janes...|\(the html file of the blog post\)|1|

Note about published: 1 means post is public (anyone can see it), 0 means unpublished (only the owner can see it)


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
