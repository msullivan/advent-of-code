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


--------

decompress ('(':xs) =
  let (lol, ys) = splitOn1 ")" xs
      [n, m] = map iread $ splitOn "x" lol
      rep = take n ys
  in (m * (decompress rep)) + decompress (drop n ys)
decompress (x:xs) = 1 + (decompress xs)
decompress [] = 0

main = answer $ decompress . trim
