if grep -q "build-c-depends: true" version; then
    echo 'result=true' >> $GITHUB_OUTPUT
else
    echo 'result=false' >> $GITHUB_OUTPUT
fi