
select
    primary_category,
    count(*) as paper_count
from {{ ref('stg_papers') }}
group by primary_category
order by paper_count desc
