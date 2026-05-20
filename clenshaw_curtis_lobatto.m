function [nodes, weights] = clenshaw_curtis_lobatto(N)
    % CLENSHAW_CURTIS_LOBATTO Computes the nodes and weights for the 
    % N-point Gauss-Lobatto quadrature rule using the Golub-Welsch algorithm
    % with a modified Jacobi tridiagonal matrix.
    %
    % Inputs:
    %   N - Number of quadrature points (must be >= 3)
    %
    % Outputs:
    %   nodes   - N-dimensional vector containing the quadrature nodes
    %   weights - N-dimensional vector containing the quadrature weights
    
    if N < 3
        error('The number of points N must be at least 3.');
    end
    
    % Step 1: Initialize the diagonal and off-diagonal elements of the
    % tridiagonal Jacobi matrix.
    % For Legendre polynomials, the diagonal elements a_i are 0.
    % The off-diagonal elements beta_i are:
    % beta_i = i / sqrt(4 * i^2 - 1) for i = 1, ..., N-2
    beta = zeros(N-1, 1);
    for i = 1:(N-2)
        beta(i) = i / sqrt(4 * i^2 - 1);
    end
    
    % Step 2: Modify the last off-diagonal element beta_{N-1} for Lobatto
    % beta_{N-1}^2 = (N-1) / (2*N - 3)
    beta(N-1) = sqrt((N - 1) / (2 * N - 3));
    
    % Step 3: Construct the symmetric tridiagonal Jacobi matrix J
    J = diag(beta, 1) + diag(beta, -1);
    
    % Step 4: Find eigenvalues (nodes) and eigenvectors of the Jacobi matrix J
    [V, D] = eig(J);
    
    % Extract the eigenvalues (nodes)
    nodes = diag(D);
    
    % Sort the nodes and match the corresponding eigenvector components
    [nodes, idx] = sort(nodes);
    V = V(:, idx);
    
    % Step 5: Compute the weights from the first component of the normalized eigenvectors
    % w_i = 2 * (v_{i,1})^2
    weights = 2 * (V(1, :).^2)';
end
