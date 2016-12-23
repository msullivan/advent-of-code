-- trying to do 19b without any clever data structures
-- this unfortunately required slightly more actualy thought about the code :P

import Control.Monad
import Data.List.Extra
import Data.Maybe

-----
type Queue a = ([a], [a])
qfromList x = (x, [])
qpush (h, t) x = (h, x:t)
qpop (x:xs, t) = (x, (xs, t))
qpop ([], t) = qpop (reverse t, [])
--------
num = 3005290

advance q = let (x, q') = qpop q in qpush q' x
kill = snd . qpop

-- if odd, advance once after delete
-- if even, none of that
step (q, n) =
  let q' = kill q
      q'' = if odd n then advance q' else q'
  in (q'', n-1)

solve n =
  let q = qfromList [1..n]
      q' = iterate advance q !! (n `div` 2)
      (qfin, _) = until ((==1) . snd) step (q', n)
  in fst $ qpop qfin


main = print $ solve num
