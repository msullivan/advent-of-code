-- XXX: doesn't work because unicode

import Data.List
import Data.List.Extra


nus :: String -> String
nus = read

lol s = show $ length s - length (nus s)
--lol s = length (show s) - length s

answer f = interact $ (++"\n") . show . f
--main = answer $ sum . map lol . lines
main = interact $ unlines . map lol . lines
