import Control.Monad
import Data.List.Extra
import Data.Maybe
import qualified Data.Char
import qualified Data.Map as Map

-- This is the first time I used monads for advent of code!

-- Input hardcoded because there are only 4 lines of it
ingredients = [[2, 0, -2, 0, 3],
               [0, 5, -3, 0, 3],
               [0, 0, 5, -1, 8],
               [0, -1, 0, 5, 8]]

-- partitions target n returns a list of all lists
-- [k_1, ..., k_n] s.t. k_1 + ... + k_n = target
partitions :: Int -> Int -> [[Int]]
partitions count 1 = [[count]]
partitions count n =
  do k <- [0..count]
     l <- partitions (count-k) (n-1)
     return (k : l)

scale k l = map (* k) l

scores =
  do coefs <- partitions 100 (length ingredients)
     let scaled = zipWith scale coefs ingredients
         final = map sum $ transpose scaled
     guard $ not (any (<0) final)
     return $ product $ take 4 final

main = putStrLn $ show $ maximum scores
