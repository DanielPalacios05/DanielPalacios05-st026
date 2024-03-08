package core

type Command interface {
	checkArguments() error
	execute() (string, error)
}
