import Control.Monad
import Data.List.Extra
import Data.Maybe
import qualified Data.Char as C
import qualified Data.Map as Map
import qualified Data.Set as Set

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
totup [x,y,z] = (x,y,z)
parse x = (chunksOf 3 x)
add = zipWith (+)
dist x = sum $ map abs x

step ([p,v,a],i) = ([p `add` v', v', a], i)
  where v' = v `add` a
stepA l = map step l

lurr (x,y) = (dist (head x), y)

pos ([p,v,a],i) = p
megaNubBy f = concat . filter ((==1).length) . groupOn f . sortOn f


part1 = map (snd . minimum . map lurr). iterate stepA
part2 = map length. iterate (megaNubBy pos . stepA)

-- Just run it until the answer is steady which happens pretty quick
main = answer $ uncurry zip . do2 part1 part2 . (flip zip) [0..] . map (parse . ireadOut) . lines
