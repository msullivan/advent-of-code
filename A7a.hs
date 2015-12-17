import Data.List
import Data.Word
import Data.Maybe
import Data.Bits
import qualified Data.Map as Map

type Signals = Map.Map String Word16

lookupSignal :: Signals -> String -> Word16
lookupSignal signals key = Map.findWithDefault (read key) key signals

computeGate :: [String] -> Signals -> Word16
computeGate cmd signals = comp cmd
  where comp [x, "AND", y] = val x .&. val y
        comp [x, "OR",  y] = val x .|. val y
        comp [x, "LSHIFT",  y] = val x `shiftL` (fromEnum $ val y)
        comp [x, "RSHIFT",  y] = val x `shiftR` (fromEnum $ val y)
        comp ["NOT",  x] = complement $ val x
        comp [x] = val x

        val = lookupSignal signals

processGate :: Signals -> String -> (String, Word16)
processGate signals cmd =
  let (gate, ["->", output]) = break (== "->") $ words cmd
  in (output, computeGate gate signals)

makeSignals :: [String] -> Signals
makeSignals cmds = signals
  -- Feed the signals back into the computation lazily
  where signals = Map.fromList $ map (processGate signals) cmds

answer f = interact $ (++"\n") . show . f
main = answer $ fromJust . Map.lookup "a" . makeSignals . lines
