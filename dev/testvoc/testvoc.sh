TMPDIR=./tmp
MONODIX_2=../../apertium-hbs-eng.hbs.dix
MONODIX_1=../../apertium-hbs-eng.eng.dix

DIRECTION=$1
PATTERN=$2

if [ -z $PATTERN ] && [ -z $DIRECTION ]; then
    echo
    echo "Example usage (full testvoc):"
    echo
    echo "  English -> BCMS: " $0 "1"
    echo "  BCMS -> English: " $0 "2"
    echo
    echo "Example usage (per pattern testvoc):"
    echo
    echo "  English -> BCMS: " $0 "1 '<np>'"
    echo "  BCMS -> English: " $0 "2 '<np>'"    
    exit
fi

if [[ $DIRECTION = "1" ]]; then 
    # TODO: The other hbs variants
    DIRECTION="eng-hbs_HR"
    TITLE="==English->BCMS===========================";
elif [[ $DIRECTION = "2" ]]; then 
    DIRECTION="hbs-eng"
    TITLE="==BCMS->English ===================";
else
    TITLE="UNKNOWN"
fi

if [ -z $PATTERN ]; then
    mkdir -p $TMPDIR
    echo $TITLE
    bash inconsistency.sh "$DIRECTION" > $TMPDIR/$DIRECTION.testvoc; 
    bash inconsistency-summary.sh $TMPDIR/$DIRECTION.testvoc $DIRECTION $MONODIX_1
    echo ""    
else
    PATTERN=$2
    mkdir -p $TMPDIR
    echo $TITLE
    bash inconsistency.sh "$DIRECTION" "$PATTERN" > $TMPDIR/$DIRECTION.testvoc; 
    bash inconsistency-summary.sh $TMPDIR/$DIRECTION.testvoc $DIRECTION $MONODIX_2
fi

# Cleanup
rm $TMPDIR/*.tmp
