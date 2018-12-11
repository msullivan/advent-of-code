import Control.Monad
import Data.List.Extra
import Data.Maybe
import qualified Data.Char as C
import qualified Data.Map as Map
import qualified Data.Set as Set
import Debug.Trace

import qualified Data.Sequence as S
import Data.Sequence ((<|), (><))

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

players = 470; num = 72170
--players = 9; num = 25

fix k l = (k + 3 * S.length l) `mod` S.length l

place (m, scores) cur k | k `mod` 23 /= 0 =
 let (a, b) = S.splitAt (fix (-1) m) m
     m' = k <| b >< a
 in (m', scores)
-- (S.insertAt (fix (-1) marbles) k marbles, scores)
place (marbles, scores) cur k =
  let v = S.index marbles (fix 7 marbles)
      m' = S.deleteAt (fix 7 marbles) marbles
      scores' = Map.insertWith (+) cur (v + k) scores
      (a, b) = S.splitAt (fix 6 m') m'
  in (b >< a, scores')

go (marbles, scores) cnt player | cnt == num = scores
go (marbles, scores) cnt player =
  go (place ({-traceShow marbles-} marbles, scores) player cnt) (cnt + 1) ((player + 1) `mod` players)

solve _ = maximum $ Map.elems $ go (start, Map.empty) 1 0
  where all = [0..num-1]
        start = S.singleton 0


main = answer $ solve
