# Makefile for PUMA with no graphics

F90=gfortran
CC=gcc

%.o : %.f90
	${F90} -c -O $<
%.o : %.c
	${CC} -c -O $<


MPIMOD=mpimod_stub
GUIMOD=guimod_stub
FFTMOD=fftmod

OBJ=${MPIMOD}.o ${FFTMOD}.o ${GUIMOD}.o resmod.o puma.o legsym.o restartmod.o pumax_stub.o gaussmod.o

puma.x:	$(OBJ)
	${F90} -o puma.x $(OBJ)

resmod.o:	resmod.f90
puma.o:		puma.f90 resmod.o
${FFTMOD}.o:	${FFTMOD}.f90
${GUIMOD}.o:	${GUIMOD}.f90 puma.o
${MPIMOD}.o:	${MPIMOD}.f90 puma.o
legsym.o:	legsym.f90 puma.o
gaussmod.o:     gaussmod.f90
restartmod.o:	restartmod.f90
pumax_stub.o:   pumax_stub.c

clean:
	rm -f *.o *.mod
