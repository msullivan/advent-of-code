import Data.Array

answer :: (Show a) => (String -> a) -> IO ()
answer f = interact $ (++"\n") . show . f

mjolt l = grid ! (0, 12)
  where
    num = 12
    len = length l
    a = listArray (0, len - 1) $ reverse l

    grid = array ((0, 0), (len, num))
      [((i, j), search (i, j)) | i <- [0..len], j <- [0..num]]

    search (start :: Int, 0 :: Int) = 0
    search (start, n) | start == len = -99999999999999999
    search (start, n) =
      max
      (grid ! (start + 1, n))
      (read [a ! start] + 10 * grid ! (start + 1, n - 1))

solve lines = sum $ map mjolt lines

main = answer $ solve . lines


--      memoize f = lookup where
--        cache1 = f []
--        cache2 = memoize $ \x -> memoize $ \xs -> f (x:xs)
--        lookup [] = cache1
--        lookup (x:xs) = cache2 x xs
