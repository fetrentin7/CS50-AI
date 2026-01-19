import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 100


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
        
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    #print(transition_model(corpus, list(corpus.keys())[0], DAMPING))

    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    #ranks = iterate_pagerank(corpus, DAMPING)
    #print(f"PageRank Results from Iteration")
    #for page in sorted(ranks):
   #     print(f"  {page}: {ranks[page]:.4f}")  
def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    #dictionary representing the probability distribution over which page a random surfer would visit next
    probab_distribution = {}
    
    number_links = len(corpus[page])

    for page in corpus:
        probab_distribution[page] = 0
    
    if number_links:
        
        for linked in corpus:
            probab_distribution[linked] = (1-damping_factor)/len(corpus)  #choosing one of the pages
        for linked in corpus[page]: 
            probab_distribution[linked] += damping_factor/number_links #choosing one of the llinks 

    else:
        for linked in corpus: 
            probab_distribution[linked] = (1/len(corpus))

    return probab_distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    dictionary = {}
    page = random.choice(list(corpus.keys()))
    sample = transition_model(corpus, page, damping_factor)

    for i in corpus:
        dictionary[i] = 0

    for i in range(1, n):
        dictionary[page] += 1
        next_page = random.choices(list(corpus.keys()), weights=sample.values(), k=1) 
        page = next_page[0] 
        
    for page in dictionary:
        dictionary[page] = dictionary[page]/n

    return dictionary

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dictionary = {}
    
    page_list = list(corpus.keys())
    N = len(page_list) #assing N to a total number of pages in corpus
    page_rank = 1/N

    for page in corpus:
        dictionary[page] = page_rank

    max = page_rank
    while max > 0.001:

        max = 0
        surfer_random = (1-damping_factor)/N

        for next_page in corpus: 
            for page in corpus[next_page]:

                #if page has no links
                if len(corpus[next_page]) == 0:
                    surfer_link = page_rank
                    
                if page in corpus[next_page]:
                    surfer_link += (dictionary[next_page]/len(corpus[next_page])) * damping_factor

            new_pagerank = surfer_random + surfer_link
            dictionary[page] = new_pagerank

        

        

    return dictionary
if __name__ == "__main__":
    main()
