import Data.List
import Data.List.Extra
import Data.Maybe
import qualified Data.Map as Map


looksay l = concatMap cleanup $ group l
  where cleanup a = [length a, head a]

input :: [Int]
input = [3,1,1,3,3,2,2,1,1,3]

-- When actually running this I definitely didn't have it as a program
-- like this, and just ran this at ghci...
answer = length $ iterate looksay input !! 40

main = putStrLn $ show answer
