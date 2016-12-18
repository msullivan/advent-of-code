import Control.Monad
import Data.List.Extra
import Data.Maybe
import qualified Data.Char as C
import qualified Data.Map as Map

--------

input = "...^^^^^..^...^...^^^^^^...^.^^^.^.^.^^.^^^.....^.^^^...^^^^^^.....^.^^...^^^^^...^.^^^.^^......^^^^"

one "^^." = '^'
one ".^^" = '^'
one "^.." = '^'
one "..^" = '^'
one _     = '.'

step s = map one $ filter ((==3) . length) $ map (take 3) $ tails ('.' : s ++ ".")

-- this stuff actually done in ghci
solve n = length $ filter (=='.') $ concat $ take n $ iterate step input
main = do print $ solve 40
          print $ solve 400000
