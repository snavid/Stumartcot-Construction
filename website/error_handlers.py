from flask import render_template, Blueprint

error_bp = Blueprint('errors', __name__)

@error_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404, error_message=str(error)), 404

@error_bp.app_errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_code=500, error_message=str(error)), 500

@error_bp.app_errorhandler(501)
def not_implemented_error(error):
    return render_template('error.html', error_code=501, error_message=str(error)), 501

@error_bp.app_errorhandler(502)
def bad_gateway_error(error):
    return render_template('error.html', error_code=502, error_message=str(error)), 502

@error_bp.app_errorhandler(503)
def service_unavailable_error(error):
    return render_template('error.html', error_code=503, error_message=str(error)), 503

@error_bp.app_errorhandler(504)
def gateway_timeout_error(error):
    return render_template('error.html', error_code=504, error_message=str(error)), 504