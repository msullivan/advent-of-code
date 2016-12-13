import Control.Monad
import Data.List.Extra
import Data.Maybe
import qualified Data.Char as C
import qualified Data.Map as Map

import Debug.Trace

faveNum = 1362
goal = (31,39)
--faveNum = 10
--goal = (7,4)


countOnes 0 = 0
countOnes n = n `mod` 2 + countOnes (n `div` 2)

isOpen (x, y) = countOnes ((x*x + 3*x + 2*x*y + y + y*y) + faveNum) `mod` 2 == 0



search seen [] = Map.size seen
search seen ((k, c@(x,y)) : rest) =
    search (Map.insert c () seen) $ rest ++
    do (i,j) <- [(-1,0), (1,0), (0,-1), (0,1)]
       let c'@(x',y') = (x+i, y+j)
       guard $ x' >= 0 && y' >= 0
       guard $ isOpen c'
       guard $ Map.notMember c' seen
       guard $ k < 50
       return (k+1, c')

--------
main = putStrLn $ show $ search Map.empty [(0, (1,1))]
