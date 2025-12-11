import Control.Monad
import Data.List
import Data.List.Split
import Data.Maybe
import qualified Data.Char as C
import qualified Data.Map as Map
import qualified Data.Set as Set
import Debug.Trace
import Memoize
-- import Data.Function.Memoize

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

parse1 l =
  let [x, outs] = splitOn ": " l
  in (x, splitOn " " outs)

parse = Map.fromList . map parse1

-- cheesy use of tuples because my "educational" version of Memoize
-- only supports pairs and not currying
solve m = memoFix search ((False, False), "svr")
  where search s ((True, True), "out") = 1
        search s ((_, _), "out") = 0
        search s ((dac, fft), st) = sum $ do
          out <- Map.findWithDefault [] st m
          return $ s ((dac || out == "dac", fft || out == "fft"), out)

main = answer $ solve . parse . lines
