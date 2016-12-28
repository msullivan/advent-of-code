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

matches k (lo,hi) = k >= lo && k <= hi
allowed ls k = not $ any (matches k) ls
solve rules = filter (allowed rules) candidates
  where candidates = sort $ map ((+1) . snd) rules

main = answer $ head . solve . map ((read *** read) . splitOn1 "-") . lines
