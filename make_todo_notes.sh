note_dir="notes"
mkdir -p $HOME/$note_dir

note_file="$HOME/$note_dir/todo.csv"

if [ ! -f $note_file ]; then
    echo '"startdate","enddate","tag","task"' > $note_file
fi

nvim -c "norm G" $note_file
