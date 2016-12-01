expr $(cat 1.input | tr -dc '(' | wc -c) - $(cat 1.input | tr -dc ')' | wc -c)
