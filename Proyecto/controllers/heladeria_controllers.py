from flask_restful import Resource
from flask import jsonify, request
from models.heladeria import Heladeria
from db import db

class HeladeriaController(Resource):

    def get(self, id=None):
        if id:
            heladeria = Heladeria.query.get_or_404(id)
            return jsonify({
                'id': heladeria.id,
                'nombre': heladeria.nombre,
                'vender': heladeria.vender
            })
        else:
            heladerias = Heladeria.query.all()
            result = []
            for heladeria in heladerias:
                result.append({
                    'id': heladeria.id,
                    'nombre': heladeria.nombre,
                    'vender': heladeria.vender
                })
            return jsonify(result)

    def post(self, nombre_producto):
        heladeria = Heladeria.query.first()  # Asumimos que hay una sola heladería
        try:
            resultado = heladeria.vender(nombre_producto)
            if resultado == "¡Vendido!":
                return jsonify({'mensaje': resultado})
            else:
                raise ValueError(resultado)
        except ValueError as e:
            return jsonify({'mensaje': f"¡Oh no! {str(e)}"})

    def put(self, id):
        data = request.json
        heladeria = Heladeria.query.get_or_404(id)
        heladeria.nombre = data['nombre']
        heladeria.vender = data['vender']
        db.session.commit()
        return jsonify({'message': 'Heladería actualizada con éxito'})

    def delete(self, id):
        heladeria = Heladeria.query.get_or_404(id)
        db.session.delete(heladeria)
        db.session.commit()
        return jsonify({'message': 'Heladería eliminada con éxito'})
