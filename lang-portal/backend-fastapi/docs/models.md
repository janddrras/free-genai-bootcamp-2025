# We have the following tables:

## words - stored vocabulary words

  - id integer
  - hungarian string
  - english string
  - parts json
## words_groups - join table for words and groups many-to-many

  - id integer
  - word_id integer
  - group_id integer
## groups - thematic groups of word s

  - id integer
  - name string
## study_sessions - records of study sessions grouping word_review_items

  - id integer
  - group_id integer
  - created_at datetime
  - study_activity_id integer
## study_activities - a specific study activity, linking a study session to group

  - id integer
  - study_session_id integer
  - group_id integer
  - created_at datetime
## word_review_items - a record of word practice, determining if the word was correct or not

  - word_id integer
  - study_session_id integer
  - correct boolean
  - created_at datetime