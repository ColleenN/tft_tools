from seed_gen.base import SeedRegistry

if __name__ == '__main__':

    for seed_class in SeedRegistry.get_registered_seeds().values():
        seed_class().write_seed_data()