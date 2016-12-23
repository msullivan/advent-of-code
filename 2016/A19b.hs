-- for part 1 I just looked up the closed form for the Josephus
-- problem on wikipedia <_<

import Control.Monad
import Data.List.Extra
import Data.Maybe
import qualified Data.Char as C
import qualified Data.Map as Map
import qualified Data.Sequence as S
import Data.Sequence ((<|), (|>), (><), ViewL(..))

--------
num = 3005290

makeSeq n = S.fromList [1..n]

step s =
  let (keep, s') = S.splitAt 1 s
      s'' = S.deleteAt ((S.length s' - 1) `div` 2) s'
  in s'' >< keep

-- done at repl
solve n = (`S.index` 0) $ until ((==1) . S.length) step $ makeSeq num
main = print $ solve num
