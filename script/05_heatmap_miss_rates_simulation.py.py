import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, ttest_1samp
#def softmax(x):
    #e_x = np.exp(x - np.max(x))
    #return e_x / e_x.sum()
beta = 1
def softmax(x):
    e_x = np.exp((x - np.max(x)) * beta)
    return e_x / e_x.sum()

def perpendicular_foot(Px, Py, Ox, Oy, m): # Foot of the perpendicular from point P to line with slope m and passing through O
    Px_, Py_ = sp.symbols('Px_ Py_')
    
    eq1 = sp.Eq(Py - Py_, (-1/m) * (Px - Px_))
    eq2 = sp.Eq(Oy - Py_, m * (Ox - Px_))
    
    solution = sp.solve((eq1, eq2), (Px_, Py_))
    
    return float(solution[Px_]), float(solution[Py_])

def signed_l(Ax,Ay,Bx,By):
    # Calculate the distance between the points
    l = np.sqrt((Ax - Bx)**2 + (Ay - By)**2)

    # Calculate the signed length based on the formula
    if (Ax - Bx) != 0:
        signed_l = l * (Ax - Bx) / np.abs(Ax - Bx)
    else:
        signed_l = 0
    return signed_l

# Given points
Ax, Ay = 2, 5
Bx, By = 5, 2

# Calculate Me (slope of AB)
Me = (Ay - By) / (Ax - Bx)

D1x,D1y = 0.8*Ax, Ay # Range Decoy targeting A
D2x,D2y = Bx, 0.8*By # Range Decoy targeting B
D11x,D11y = Bx+ 0.2*Ax, By

p_A_baseline_values = []
P_c1_choice_values = []
P_c2_choice_values = []
ast_values = []
asc_values = []
rst_ew_values = []
rst_uw_values = []
del_p_a_values = []
del_p_b_values = []
beta_values = []
del_P_avg_values = []
miss_values = []
# Simulation parameters
sample_size = 30
quantization_bins = 20
simulated_exp = 10
# Define the range of population mean and variance values
mu_range = np.linspace(-1.2, -0.8, num=quantization_bins)
sigma_range = np.linspace(0.01, 0.05, num=quantization_bins)

# Initialize an empty array to store miss rates
missExp_rates = np.zeros((quantization_bins, quantization_bins))
miss_rates = np.zeros((quantization_bins, quantization_bins))

for i, mu_Mi in enumerate(mu_range):
    for j, sigma_Mi in enumerate(sigma_range):
        miss_values = []
        miss_exp = 0
        for k in range(simulated_exp):
            p_A_baseline_values = []
            P_c1_choice_values = []
            P_c2_choice_values = []
            ast_values = []
            asc_values = []
            rst_ew_values = []
            rst_uw_values = []
            del_p_a_values = []
            del_p_b_values = []
            beta_values = []
            del_P_avg_values = []

            misses = 0
            mi_values = np.random.normal(loc=mu_Mi, scale=sigma_Mi, size=sample_size)
            for Mi in mi_values:
                Bx_, By_ = perpendicular_foot(Bx, By, Ax, Ay, Mi)
                d = signed_l(Bx,By,Bx_,By_)
                # Calculate the softmax-transformed value of d
                baseline = softmax([0, d])
                p_A_baseline_values.append(baseline[0])

                D1x_,D1y_ = perpendicular_foot(D1x, D1y, Ax, Ay, Mi)
                d1 = signed_l(D1x,D1y,D1x_,D1y_)  

                D2x_,D2y_ = perpendicular_foot(D2x, D2y, Ax, Ay, Mi)
                d2 = signed_l(D2x,D2y,D2x_,D2y_)

                #Attraction in C2, reversed attraction in C1
                if D2y <= Ay-Mi*(Ax-Bx) <= By: #SIC through A passing between B & D2
                    beta = 4.5               # clear dominance is perceived between B & D2
                    choice_c1 = softmax([0, d, d1]) # in context {A,B,D2} & in {A,B,D1} A& D1 lie
                    choice_c2 = softmax([0, d, d2]) # same side of SIC passing through B, treated similar and reversed attraction
                    #beta = 1 # reset beta
                    #print('SIC through A pssing between B & D2')
                    #print('D2 dominated, choice_c2: ',choice_c2)
                    #print('D1 perceived similar to A, choice_c1: ',choice_c1)
                #Attraction in C1, reversed attraction in C2
                elif Bx <= Ax - (Ay-By)*1/Mi <= D11x:
                    beta = 4.5
                    choice_c1 = softmax([0, d, d1])
                    choice_c2 = softmax([0, d, d2])
                    #print('SIC through B passing between A & D1')
                    #print('D1 dominated, choice_c1: ',choice_c1)
                    #print('D2 perceived similar to B, choice_c2: ',choice_c2)
                else:
                    beta = 1
                    choice_c1 = softmax([0, d, d1])
                    choice_c2 = softmax([0, d, d2]) 
                # if beta != 1:
                #     context_effect_flag.append(1)
                P_c1_choice_values.append(choice_c1)
                P_c2_choice_values.append(choice_c2)
                beta_values.append(beta)
                beta = 1

                rst_1 = choice_c1[0]/(choice_c1[0]+choice_c1[1])
                rst_2 = choice_c2[1]/(choice_c2[0]+choice_c2[1])
                rst_ew = 0.5*(rst_1+rst_2)
                rst_ew_values.append(rst_ew)

                rst_uw = (choice_c1[0]+choice_c2[1])/(choice_c1[0]+choice_c2[1]+choice_c1[1]+choice_c2[0])
                rst_uw_values.append(rst_uw)

                ast_1 = (choice_c1[0]/(choice_c1[0]+choice_c1[1]+choice_c1[2]))
                ast_2 = (choice_c2[1]/(choice_c2[0]+choice_c2[1]+choice_c1[2]))
                ast = 0.5* (ast_1 + ast_2)
                ast_values.append(ast)

                asc_1 = (choice_c1[1]/(choice_c1[0]+choice_c1[1]+choice_c1[2]))
                asc_2 = (choice_c2[0]/(choice_c2[0]+choice_c2[1]+choice_c1[2]))
                asc = 0.5* (asc_1 + asc_2)
                asc_values.append(asc)

                del_p_a = choice_c1[0]-choice_c2[0]
                del_p_b = choice_c2[1]-choice_c1[1]
                del_p_a_values.append(del_p_a)
                del_p_b_values.append(del_p_b)

                del_P_a_c1 = choice_c1[0]-baseline[0]
                del_P_a_c2 = choice_c2[0]-baseline[0]
                del_P_b_c1 = choice_c1[1]-baseline[1]
                del_P_b_c2 = choice_c2[1]-baseline[1]
            #     del_P_c1 = max(del_P_a_c1, del_P_b_c1)
            #     del_P_c2 = max(del_P_a_c2, del_P_b_c2)
            #     del_P_avg = 0.5*(del_P_c1 + del_P_c2)
                del_P_avg = max(del_P_a_c1,del_P_a_c2,del_P_b_c1,del_P_b_c2)
                del_P_avg_values.append(del_P_avg)#This measure will reflect the true effect in a pair-triplet design.



            #     print('p_rst : ', p_rst, 'RST :',rst_uw)
            #     print('p_del_P : ',p_del_P, 'del_P : ', del_P_avg)
            #     print('misses: ', misses, "miss_exp: ", miss_exp)
                print('RST :',rst_uw, 'del_P : ', del_P_avg)
                if (rst_uw < 0.5) and (del_P_avg > 0):
                    misses +=1
            miss_values.append(misses)
            # Conduct one-sample t-test
            t_rst, p_rst = ttest_1samp(rst_uw_values, 0.5,  alternative='less')
            t_del_P, p_del_P = ttest_1samp(del_P_avg_values, 0, alternative = 'greater')
            # Check for Misses
            if (p_rst < 0.5) and (p_del_P < 0.5) : 
                miss_exp += 1
            print('p_rst : ', p_rst, 'p_del_P : ',p_del_P)
            print('mu : ', mu_Mi, 'sigma : ', sigma_Mi, 'misses: ', misses, "miss_exp: ", miss_exp)
            # Store the result in the array
        print('miss_rate :', miss_exp/simulated_exp)
        print('misses_avg: ', sum(miss_values)/simulated_exp)
        # Store the result in the array
        missExp_rates[i, j] = miss_exp/simulated_exp
        miss_rates[i, j] = sum(miss_values)/simulated_exp
# Create a 2D heatmap for miss rates
plt.imshow(miss_rates/30, extent=[sigma_range.min(), sigma_range.max(), mu_range.min(), mu_range.max()], aspect='auto', cmap='viridis')
plt.colorbar(label='Miss Rate')
plt.xlabel('Population Variance (sigma_Mi)')
plt.ylabel('Population Mean (mu_Mi)')
# plt.title('2D Heatmap of Miss Rates')
#plt.show()
plt.grid(True)
plt.savefig('Heatmap of MissRates25', dpi=1200, bbox_inches="tight")
plt.show()


# Create a 2D heatmap for miss rates 
plt.imshow(missExp_rates, extent=[sigma_range.min(), sigma_range.max(), mu_range.min(), mu_range.max()],
           aspect='auto', cmap='viridis')
plt.colorbar(label='Miss Rate (Exp)')
plt.xlabel('Population Variance (sigma_Mi)')
plt.ylabel('Population Mean (mu_Mi)')
# plt.title('2D Heatmap of Miss Rates')
#plt.show()
plt.grid(True)
plt.savefig('Heatmap of MissRates_Exp', dpi=1200, bbox_inches="tight")
plt.show()
import pdb;

pdb.set_trace()
