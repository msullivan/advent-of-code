-- both parts
-- this was sort of slamming together day 13 and day 14 >_>

-- I normally try to save the part 1 if part 2 involved any nontrivial
-- modifications, but I forgot. The modifications were pretty simple
-- though. In part 1, search just returned the shortest path, so it
-- only returned one string and didn't have a base case.

import Control.Monad
import Data.List.Extra
import Data.Maybe
import qualified Data.Char as C
import qualified Data.Map as Map
import qualified Crypto.Hash.MD5 as MD5
import qualified Data.ByteString.Char8 as BS
import qualified Data.ByteString.Base16 as B16
import Debug.Trace

--
md5 = BS.unpack . B16.encode . MD5.hash . BS.pack
--

key = "njfxhljp"
--key = "ulqzkmiv"
goal = (3,3)

search [] = []
search ((path, loc@(x,y)) : rest) =
  if loc == goal then reverse path : search rest else
    search $ rest ++
    do let hash = md5 (key ++ reverse path)
       let valid = map (\x -> not (C.isDigit x || x == 'a')) hash
       (good, (i,j,dir)) <- zip valid [(0,-1,'U'), (0,1,'D'), (-1,0,'L'), (1,0,'R')]
       guard good
       let c'@(x',y') = (x+i, y+j)
       guard $ x' >= 0 && y' >= 0
       guard $ x' < 4 && y' < 4
       return (dir:path, c')

--------
-- actually just did stuff in ghci when actually doing it
main = do putStrLn $ head paths
          putStrLn $ show $ maximum $ map length $ paths
  where paths = search [([], (0,0))]
