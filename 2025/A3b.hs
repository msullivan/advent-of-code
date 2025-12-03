import Control.Monad
import Data.List
import Data.Array
import Data.List.Split
import Data.Maybe
import qualified Data.Char as C
import qualified Data.Map as Map
import qualified Data.Set as Set
import Data.Function.Memoize
import Debug.Trace

------
iread :: String -> Int
iread = read

do2 f g x = (f x, g x)

answer :: (Show a) => (String -> a) -> IO ()
answer f = interact $ (++"\n") . show . f

ord0 c = C.ord c - C.ord 'a'
chr0 i = C.chr (i + C.ord 'a')
incletter c i = chr0 ((ord0 c + i) `mod` 26)

-- splitOn1 a b = fromJust $ stripInfix a b
-- rsplitOn1 a b = fromJust $ stripInfixEnd a b

-- pull out every part of a String that can be read in
-- for some Read a and ignore the rest
readOut :: Read a => String -> [a]
readOut "" = []
readOut s = case reads s of
  [] -> readOut $ tail s
  [(x, s')] -> x : readOut s'
  _ -> error "ambiguous parse"
ireadOut :: String -> [Int]
ireadOut = readOut

traceShow' s = traceShow s s

--------

mjolt l = search (0, 12)
  where
    len = length l
    a = listArray (0, len - 1) $ reverse l

    fsearch _ (start :: Int, 0 :: Int) = 0
    fsearch _ (start, n) | start == len = -99999999999999999
    fsearch search (start, n) =
      max
      (search (start + 1, n))
      (read [a ! start] + 10 * search (start + 1, n - 1))
    search = memoFix fsearch

parse = id

solve lines = sum $ map mjolt lines

main = answer $ solve . lines
