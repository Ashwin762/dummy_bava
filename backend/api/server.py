from fastapi import FastAPI

from api.routes import router as api_router


def create_app() -> FastAPI:
	app = FastAPI(
		title="Dummy Bava Job API",
		version="1.0.0",
		description="Backend APIs for job search, listing, and export metadata.",
	)

	@app.get("/")
	def healthcheck() -> dict:
		return {"success": True, "message": "API is running", "data": {"status": "ok"}}

	app.include_router(api_router)
	return app


app = create_app()
