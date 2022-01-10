from analyse_scores import refresh_analysed_scores
from crypto_tracker import crypto_tracker
from query_reddit import query_reddit

if __name__ == "__main__":
    crypto_tracker.main()
    query_reddit.main()
    refresh_analysed_scores.main()
