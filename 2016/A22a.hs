import Control.Monad
import Data.List.Extra
import Data.Maybe
import qualified Data.Char as C
import qualified Data.Map as Map

------
iread :: String -> Int
iread = read

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
munge [a,b,c,d,e,f] = ((a,b), (c,d,e,f))

viable (c, (_, used, _, _)) (c', (_, _, avail, _)) =
  c /= c' && avail >= used && used > 0

findMatch stuff c = map (\x -> (c,x)) $ filter (viable c) stuff
getallviable ls = concatMap (findMatch ls) ls

main = answer $ length . getallviable . map (munge . ireadOut) . lines
--main = answer $ length $ map (munge . ireadOut) . lines
