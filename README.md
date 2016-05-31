# Job Recommendations

1. Can we determine the most important data science skills?
2. Are there distinguishable language qualities that separate one job description from another?
3. Would it be possible to group job descriptions based on specific tones, sentiment, or topics?


| Aspect        | Approach      |
| ------------- |-------------|
| Setup, Design      | Spot checking, Individual brainstorming  |
| Data               | 10,000 different Data Science job descriptions from Indeed.com   |
| Modeling           | Unsupervised Learning; Latent Semantic Indexing, Latent Dirichlet Allocation, Approximate Nearest Neighbors, keyword extraction     |
| Tools         | nltk; gensim; scikit-learn; MongoDB; Flask; AWS  |


- Create a generalized web scraping tool.
- Initial understanding and exploratory analysis
- Produce a weighted word vector matrix (TF-IDF)
- Identify patterns and relationships between terms (LSI + SVD)
- Determine observable similarities
