from app import run_lexer, run_parser, run_interpreter

def main():
	while True:
		print('Press CTRL+C to exit')
		text = input('utconv >>> ')

		# Tokens
		tokens = run_lexer(text)
		tokensStr = ', '.join(map(lambda n: repr(n), tokens))
		print(f'Tokens: {tokensStr}')

		# Tree
		root = run_parser(tokens)
		print(f'Nodes: {root}')

		# Simplify nodes
		root.simplify()
		print(f'Nodes Simplified: {root}')

		# Run interpreter
		result = run_interpreter(root)
		print(f'Result: {result}')

		# Simplify result
		result.simplify()
		print(f'Result Simplified: {result}')


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass