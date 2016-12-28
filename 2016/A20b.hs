-- OK so this version actually works.
-- But I actually somewhat accidentally originally solved this problem by
-- taking the length of the list that I produced in part 1...
-- None of the gaps are longer than 1 element!

-- This code could also produce the part 1 solution more efficient
-- than part 1, though it doesn't seem to matter.

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

rmerge (lo,hi) ((lo',hi'):rest) =
  if lo' <= hi+1 then rmerge (lo,max hi hi') rest
  else (lo,hi) : rmerge (lo',hi') rest
rmerge (lo,hi) [] = [(lo,hi)]

canonify l = rmerge (-1,-1) $ sort $ (maxNum,maxNum):l

gap (_,hi) (lo,_) = lo-hi-1

solve l = sum $ zipWith gap l (tail l)

main = answer $ solve . canonify . map ((read *** read) . splitOn1 "-") . lines
