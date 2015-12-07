import Data.List
import Data.List.Extra
import Data.Word
import Data.Maybe
import Data.Bits
import qualified Data.Map as Map

type Signals = Map.Map String Word16

lookupSignal :: Signals -> String -> Word16
lookupSignal signals key =
  case Map.lookup key signals of
    Just v -> v
    Nothing -> read key


computeGate :: [String] -> Signals -> Word16
computeGate cmd signals = comp cmd
  where comp [x, "AND", y] = val x .&. val y
        comp [x, "OR",  y] = val x .|. val y
        comp [x, "LSHIFT",  y] = val x `shiftL` (fromEnum $ val y)
        comp [x, "RSHIFT",  y] = val x `shiftR` (fromEnum $ val y)
        comp ["not",  x] = complement $ val x
        comp [x] = val x

        val = lookupSignal signals

processGate :: Signals -> String -> Signals
processGate signals cmd =
  let (gate, ["->", output]) = break (== "->") $ words cmd
  in Map.insert output (computeGate gate signals) signals



answer f = interact $ (++"\n") . show . f
main = answer $ fromJust . Map.lookup "a" . foldl processGate Map.empty . lines
