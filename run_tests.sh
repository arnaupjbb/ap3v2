g++ checker.cc -o checker
codon build metaheur_vgrasp.py

time(for i in {1..20}; do
    # Run Python script and redirect input/output
    ./metaheur_vgrasp sort.txt < "public_benchs/hard-$i.txt"
    cat sort.txt >> output.txt

    # Run the compiled checker
    ./checker "public_benchs/hard-$i.txt" sort.txt
done)