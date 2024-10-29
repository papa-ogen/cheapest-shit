all:
	uvicorn main:app --reload & cd frontend && npm run dev



