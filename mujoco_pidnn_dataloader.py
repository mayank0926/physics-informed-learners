import numpy as np
import mujoco_collection_constants as mcc
import torch
from pyDOE import lhs

VT_test = None
X_test = None

def testset_loss(model):
	with torch.no_grad():
		X_pred = model.forward(VT_test)
	error_vec = torch.linalg.norm((X_test-X_pred),2)/torch.linalg.norm(X_test,2)		# Relative L2 Norm of the error (Vector)
	X_pred = X_pred.cpu().detach().numpy()
	X_pred = np.reshape(X_pred,(mcc.vx_range.shape[0],mcc.t_range.shape[0]),order='F')
	return error_vec, X_pred


def dataloader(N_u, N_f, device, N_validation=0):
	""" N_u = training data / boundary points for data driven training
	N_f = collocation points for differential for differential driven training
	"""

	data = np.genfromtxt(mcc.filename, delimiter=',')
	data = np.array(data, dtype=np.float32)

	assert data.shape[0] == mcc.TOTAL_ITERATIONS
	assert data.shape[1] == mcc.vx_range.shape[0]

	vrange = mcc.vx_range
	trange = mcc.t_range
	xrange = data

	V, T = np.meshgrid(vrange,trange)
	VT_true = np.hstack((V.flatten()[:,None], T.flatten()[:,None]))
	X_true = np.array(xrange.flatten('C')[:,None])
	# Now ith column of VT corresponds to ith column of X

	lb = np.min(VT_true, axis=0)
	ub = np.max(VT_true, axis=0)

	if mcc.training_is_border:
		VT_indices = np.arange(VT_true.shape[0])
		VT_basecase_indices = VT_indices[np.logical_or(VT_true[:,0] == 0, VT_true[:,1] == 0)]

		idx = VT_basecase_indices[np.random.choice(VT_basecase_indices.shape[0], N_u, replace=False)]
		VT_u_train = VT_true[idx, :]
		X_u_train = X_true[idx, :]
	else:
		idx = np.random.choice(VT_true.shape[0], N_u, replace=False)
		VT_u_train = VT_true[idx, :]
		X_u_train = X_true[idx, :]

	
	VT_f_train = lb + (ub-lb)*lhs(2, N_f)
	VT_f_train = np.vstack((VT_f_train, VT_u_train))

	# Convert all to tensors

	VT_u_train = torch.from_numpy(VT_u_train).float().to(device)
	X_u_train = torch.from_numpy(X_u_train).float().to(device)
	VT_f_train = torch.from_numpy(VT_f_train).float().to(device)

	global VT_test, X_test
	VT_test = torch.from_numpy(VT_true).float().to(device)
	X_test = torch.from_numpy(X_true).float().to(device)

	return VT_u_train, X_u_train, VT_f_train, lb, ub
