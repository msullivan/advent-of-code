import Data.List
import Data.List.Extra

-- Originally done in python but I redid it in haskell to get back in
-- the feel of writing haskell (which I don't think I've done since
-- last year's AoC).

iread :: String -> Int
iread = read

check :: [Int] -> Bool
check x = let [a,b,c] = sort x
          in a+b > c

load = map iread . words

fux = concat . map transpose . chunksOf 3

answer f = interact $ (++"\n") . show . f
main = answer $ length . filter check . fux . map load . lines
