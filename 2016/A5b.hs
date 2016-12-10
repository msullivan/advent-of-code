import Data.List
import Data.Maybe
import Data.Hash.MD5
import Debug.Trace

key = "reyedfim"

traceSelf x = traceShow x x

result = map (fromJust . flip lookup stuff . show) [0..7]
  where stuff = map (\s -> traceSelf ([s !! 5], s !! 6)) $ filter (isPrefixOf "00000") $ map (\i -> md5s $ Str $ key ++ show i) [1..]

main = putStrLn $ show result
