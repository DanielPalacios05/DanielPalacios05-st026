package core

type Controller struct {
	MainCommand Command
}

func (c *Controller) Init() (string, error) {
	err := c.MainCommand.checkArguments()

	if err != nil {
		return "", err
	}

	result, err := c.MainCommand.execute()

	return result, err
}
