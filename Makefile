compile:
	brownie compile

deploy:
	brownie run deploy

deploy_rinkeby:
	brownie run deploy --network rinkeby

test:
	brownie test

coverage:
	brownie test --coverage
