import sys
import crawler
import time

# crawler.run_comments_hepsiburada()
# crawler.run_trendyol()

if sys.argv[1] == "prod_details":
    crawler.run_prod_details_hepsiburada()

if sys.argv[1] == "comment_details":
    crawler.run_comments_hepsiburada()
