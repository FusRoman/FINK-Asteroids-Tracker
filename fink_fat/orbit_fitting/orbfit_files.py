import os
import traceback
import logging
import glob
import numpy as np


def write_inp(ram_dir, first_designation, second_designation=None):
    """
    Write the input files of Orbfit in orbit identification mode. Two designations need to be given corresponding to the both arcs.

    Parameters
    ----------
    ram_dir : string
        the path where to write the temporary file generated by orbfit.
    first_designation : string
        the provisional designation of the first arc
    second_designation : string
        the provisional designation of the second arc

    Return
    ------
    None
    """
    if second_designation is None:
        with open(ram_dir + first_designation + ".inp", "wt") as file:
            file.write(ram_dir + first_designation)
    else:
        with open(
            ram_dir + first_designation + "_" + second_designation + ".inp", "wt"
        ) as file:
            file.write(ram_dir + first_designation + "_" + second_designation)

def oop_options(
    file,
    ram_dir,
    first_desig,
    second_desig=None,
    with_ephem=0,
    ):
        # write output options
        file.write("output.\n")
        file.write("\t.elements = 'KEP'\n")

        # write operations options
        file.write("operations.\n")
        file.write("\t.init_orbdet = 2\n")
        file.write("\t.diffcor = 2\n")
        file.write("\t.ident = 2\n")

        if with_ephem not in [0, 1, 2]:
            with_ephem = 0
        file.write("\t.ephem = {}\n".format(with_ephem))

        # write error model options
        file.write("error_model.\n")
        file.write("\t.name='fcct14'\n")

        # write additional options
        file.write("IERS.\n")
        file.write("\t.extrapolation = .T.\n")

        # write reject options
        file.write("reject.\n")
        file.write("\t.rejopp = .FALSE.\n")

        # write propagation options
        file.write("propag.\n")
        file.write("\t.iast = 17\n")
        file.write("\t.npoint = 600\n")
        file.write("\t.dmea = 0.2d0\n")
        file.write("\t.dter = 0.05d0\n")

        # write location files options
        file.write(".filbe=" + ram_dir + "AST17\n")
        file.write("\noutput_files.\n")

        if second_desig is None:
            file.write("\t.elem = " + ram_dir + first_desig + ".oel\n")
        else:
            file.write(
                "\t.elem = "
                + ram_dir
                + first_desig
                + "_"
                + second_desig
                + ".oel\n"
            )
        
        file.write("object1.\n")
        file.write("\t.obs_dir = " + ram_dir + "mpcobs\n")
        file.write("\t.name = " + first_desig)

        if second_desig is not None:
            # write second object location
            file.write("\nobject2.\n")
            file.write("\t.obs_dir = " + ram_dir + "mpcobs\n")
            file.write("\t.name = " + second_desig)


def write_oop(ram_dir, first_designation, second_designation=None):
    """
    Write the option file of OrbFit in orbit identification mode. Two designations need to be given corresponding to the both arcs.

    Parameters
    ----------
    ram_dir : string
        the path where to write the temporary file generated by orbfit.
    first_designation : string
        the provisional designation of the first arc
    second_designation : string
        the provisional designation of the second arc

    Return
    ------
    None
    """
    if second_designation is None:
        with open(ram_dir + first_designation + ".oop", "w") as file:
            oop_options(file, ram_dir, first_designation)
    else:
        with open(
            ram_dir + first_designation + "_" + second_designation + ".oop", "w"
        ) as file:
            oop_options(file, ram_dir, first_designation, second_desig=second_designation)


def prep_orbitfit(ram_dir):
    """
    Preparation for OrbFit computation

    Copy the AST17 ephemeris files needed for the orbfit computation to the correct location.
    Set their permissions to be read by OrbFit.

    Parameters
    ----------
    ram_dir : string
        path where to write file

    Returns
    -------

    Examples
    --------

    >>> prep_orbitfit("")

    >>> st = os.stat("AST17.bai")
    >>> stat.filemode(st.st_mode)
    '-rwxrwxrwx'

    >>> st = os.stat("AST17.bep")
    >>> stat.filemode(st.st_mode)
    '-rwxrwxrwx'

    >>> shutil.rmtree("mpcobs")
    >>> os.remove("AST17.bai")
    >>> os.remove("AST17.bep")
    """

    try:
        fink_fat_path = os.path.dirname(__file__)
        orbfit_path = os.path.join(fink_fat_path, "orbit_fitting")
        dir_path = ram_dir + "mpcobs/"

        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)

        os.symlink(os.path.join(orbfit_path, "AST17.bai_431_fcct"), ram_dir + "AST17.bai")
        os.chmod(ram_dir + "AST17.bai", 0o777)

        os.symlink(os.path.join(orbfit_path, "AST17.bep_431_fcct"), ram_dir + "AST17.bep")
        os.chmod(ram_dir + "AST17.bep", 0o777)
    except Exception:
        logging.error(traceback.format_exc())


def rm_files(files):
    """
    Remove all files contains in the files parameters

    Parameters
    files : string list
        A list of files path (typically return by the glob library)

    Return
    ------
    None
    """
    for path_f in files:
        os.remove(path_f)


def obs_clean(ram_dir, prov_desig):
    """
    Remove all the temporary file named as prov_desig created during the OrbFit process.

    Parameters
    ----------
    ram_dir : string
        Path where files are located
    prov_desig : string
        the provisional designation of the trajectory that triggered the OrbFit process.

    Returns
    -------
    None

    Examples
    --------

    >>> prov_desig = "A000001"
    >>> open(prov_desig + ".oel", 'a').close()
    >>> open(prov_desig + ".err", 'a').close()

    >>> os.makedirs("mpcobs")
    >>> open("mpcobs/" + prov_desig + ".obs", 'a').close()
    >>> open("mpcobs/" + prov_desig + ".rwo", 'a').close()

    >>> obs_clean("", prov_desig)

    >>> os.rmdir("mpcobs")
    """

    rm_files(glob(ram_dir + prov_desig + ".*"))
    rm_files(glob(ram_dir + "mpcobs/" + prov_desig + ".*"))


def final_clean(ram_dir):
    """
    Remove the residuals files used by OrbFit

    Parameters
    ----------
    ram_dir : string
        Path where files are located

    Returns
    -------
    None

    Examples
    --------
    >>> prep_orbitfit("")

    >>> os.path.exists("AST17.bai")
    True
    >>> os.path.exists("AST17.bep")
    True
    >>> os.path.exists("mpcobs")
    True

    >>> final_clean("")

    >>> os.path.exists("AST17.bai")
    False
    >>> os.path.exists("AST17.bep")
    False
    >>> os.path.exists("mpcobs")
    False
    """
    rm_files(glob(ram_dir + "*.bai"))
    rm_files(glob(ram_dir + "*.bep"))
    rm_files(glob(ram_dir + "*.log"))

    os.rmdir(ram_dir + "mpcobs")


def read_oel_lines(lines):
    ref_mjd = float(lines[8].strip().split()[1])
    # conversion from modified julian date to julian date
    ref_jd = ref_mjd + 2400000.5

    orb_params = " ".join(lines[7].strip().split()).split(" ")
    if len(lines) > 12:
        rms = " ".join(lines[12].strip().split()).split(" ")
    else:
        rms = [-1, -1, -1, -1, -1, -1, -1, -1]
    return [ref_jd] + orb_params[1:] + rms[2:]

def read_oel(ram_dir, first_desig, second_desig=None):
    """
    Read the .oel file return by orbfit. This file contains the orbital elements, the reference epoch of the orbit computation and
    the rms of the orbital elements

    Parameters
    ----------
    ram_dir : string
        Path where files are located
    prov_desig : string
        the provisional designation of the trajectory that triggered the OrbFit process.

    Returns
    -------
    orb_elem : integer list
        A list with the reference epoch first then the orbital elements and finally the rms.

    Examples
    --------
    >>> read_oel("fink_fat/test/call_orbfit/", "K21E00A")
    [2459274.810893373, '1.5833993623527698E+00', '0.613559993695898', '5.9440877456670', '343.7960539272898', '270.1931234374459', '333.9557366497585', -1, -1, -1, -1, -1, -1]

    >>> read_oel("", "")
    [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]

    >>> read_oel("fink_fat/test/call_orbfit/", "K21H00A")
    [2459345.797868819, '3.1514694062448680E+00', '0.113946062348132', '1.6879159876457', '38.1016474068882', '136.1915246941109', '46.5628893357021', '7.94527E-03', '1.83696E-02', '4.77846E-02', '3.17863E-01', '1.34503E+01', '9.82298E+00']
    """
    try:
        if second_desig is None:
            with open(ram_dir + first_desig + ".oel") as file:
                lines = file.readlines()
                return read_oel_lines(lines)
        else:
            with open(ram_dir + first_desig + "_" + second_desig + ".oel") as file:
                lines = file.readlines()
                return read_oel_lines(lines)

    except FileNotFoundError:
        return list(np.ones(13, dtype=np.float64) * -1)
    except Exception as e:
        print("----")
        print(e)
        print()
        print("ERROR READ OEL FILE: {}".format(first_desig))
        print()
        print(lines)
        print()
        print()
        logging.error(traceback.format_exc())
        print("----")
        return list(np.ones(13, dtype=np.float64) * -1)


def read_rwo(ram_dir, prov_desig, nb_obs):
    """
    Read the .rwo file return by orbfit. This file contains the observations of the trajectories and the goodness of the fit computed by OrbFit.
    Return the chi values for each observations.

    Parameters
    ----------
    ram_dir : string
        Path where files are located
    prov_desig : string
        the provisional designation of the trajectory that triggered the OrbFit process.

    Returns
    -------
    chi : integer list
        The list of all chi values of each observations.

    Examples
    --------
    """
    try:
        with open(ram_dir + "mpcobs/" + prov_desig + ".rwo") as file:
            lines = file.readlines()

            chi_obs = [obs_l.strip().split(" ")[-3] for obs_l in lines[7:]]

            return np.array(chi_obs).astype(np.float32)
    except FileNotFoundError:
        return list(np.ones(nb_obs, dtype=np.float64) * -1)
    except ValueError:
        return list(np.ones(nb_obs, dtype=np.float64) * -1)
    except Exception as e:
        print("----")
        print(e)
        print()
        print("ERROR READ RWO FILE: {}".format(prov_desig))
        print()
        print(lines)
        print()
        print()
        logging.error(traceback.format_exc())
        print("----")
        return list(np.ones(nb_obs, dtype=np.float64) * -1)
