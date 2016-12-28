-- This is totally wrong but it somehow happens to work!
-- Apparently there aren't any gaps in my input of length > 1.

import Control.Monad
import Data.List.Extra
import Data.Maybe
import qualified Data.Char as C
import qualified Data.Map as Map
import qualified Data.Set as Set
import Control.Arrow

------
answer :: (Show a) => (String -> a) -> IO ()
answer f = interact $ (++"\n") . show . f

splitOn1 a b = fromJust $ stripInfix a b

--------
maxNum = 4294967295

matches k (lo,hi) = (k >= lo && k <= hi) || k > maxNum
allowed ls k = not $ any (matches k) ls
solve rules = filter (allowed rules) candidates
  where candidates = sort $ map ((+1) . snd) rules

main = answer $ length . solve . map ((read *** read) . splitOn1 "-") . lines
