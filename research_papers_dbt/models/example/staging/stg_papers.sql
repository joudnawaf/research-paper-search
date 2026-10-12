
select
    arxiv_id,
    version,
    trim(title) as title,
    trim(summary) as summary,
    authors,
    primary_category,
    categories,
    published,
    updated,
    pdf_url
from public.papers
where title is not null
  and trim(title) != ''
