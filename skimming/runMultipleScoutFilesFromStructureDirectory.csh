#just modify the below path to run multiple datasets
rm filelist*.txt
rm temp*.txt
set k = 1
set maxk = 9
while ( $k < $maxk )
    #modify the path below by hand (for now)
    python hlt_ScoutFilesFromStructureDirectory.py -p /eos/cms//store/data/Run2018D/EphemeralZeroBias${k}/RAW/v1/000/321/755/00000/ -f temp${k}.txt
    @ k++
end

cat temp*.txt > filelist.txt
echo "filelist.txt was created"
