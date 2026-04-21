import onnxruntime as ort

session = ort.InferenceSession("backend/model/vit_final_amd.onnx")

print("=== INPUTS ===")
for inp in session.get_inputs():
    print(f"  name: {inp.name}")
    print(f"  shape: {inp.shape}")
    print(f"  dtype: {inp.type}")

print("\n=== OUTPUTS ===")
for out in session.get_outputs():
    print(f"  name: {out.name}")
    print(f"  shape: {out.shape}")
    print(f"  dtype: {out.type}")

print("\n=== MODEL METADATA ===")
meta = session.get_modelmeta()
print(f"  producer: {meta.producer_name}")
print(f"  graph name: {meta.graph_name}")
print(f"  description: {meta.description}")
print(f"  custom metadata: {meta.custom_metadata_map}")