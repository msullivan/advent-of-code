import Control.Monad
import Data.List.Extra
import Data.Maybe
import qualified Data.Char as C
import qualified Data.Map as Map
import qualified Data.Set as Set
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

splitOn1 a b = fromJust $ stripInfix a b
rsplitOn1 a b = fromJust $ stripInfixEnd a b

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

--------

traceShow' s = traceShow s s

parse line = (m, n)
  where m = if head line == 'L' then (-1) else 1
        n = iread $ tail line

step (pos, cnt) (m, n) =
  let npos = (pos + m*n)
      pos' = npos `mod` 100
  in
    (
      pos',
      cnt + (if pos' == 0 then 1 else 0)
    )

iterN f p n = iterate f p !! n

solve = snd . foldl step (50, 0)
-- lol this ends up being noticably slow
solve2 = snd . foldl step (50, 0) . concatMap (\(m, n) -> replicate n (m, 1))
-- this too
-- stepi p (m, n) = iterN (`step` (m, 1)) p n
-- stepi p (m, n) = iterate (\x -> step x (m, 1)) !! n
-- solve2 = snd . foldl stepi (50, 0)



main = answer $ do2 solve solve2 . map parse . lines
